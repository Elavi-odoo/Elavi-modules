/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';


//the first starting function
// Fallback implementation with the same hide/show logic
$(document).ready(function() {
    console.log('📄 Document ready - Adding fallback email check');

    $(document).on('blur', 'input[type="email"], .event_attendee_email_field', function(e) {
        console.log('📧 FALLBACK: Email blur event detected');
        checkEmailFallback(e);
    });



    async function checkEmailFallback(ev) {
        const email = ev.currentTarget.value.trim();
        const emailField = ev.currentTarget;

        // Clear previous state
        clearPortalMessageFallback(emailField);
        showSubmitButtonFallback();

        if (!email || !isValidEmailFallback(email)) {
            if (email && !isValidEmailFallback(email)) {
                showPortalMessageFallback(emailField, null, 'Please enter a valid email address doc');
            }
            // Don't block submit for invalid/empty emails
            const submitButton = $('.js_submit_button');
            const form = submitButton.closest('form');
            form.off('submit.emailcheck');
            return;
        }

        // Add block submit immediately when checking starts - only for valid emails
        const submitButton = $('.js_submit_button');
        const form = submitButton.closest('form');
        console.log("submitButton", submitButton);

        // Store if this check was triggered by a submit attempt
        const isSubmitTriggered = sessionStorage.getItem('emailCheckTriggeredBySubmit') === 'true';

        // Block submission while checking valid email
        if (submitButton.length > 0 && email) {
            console.log("Blocking submit while checking email");
            form.off('submit.emailcheck').on('submit.emailcheck', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log("Form submission blocked - checking email");

                // Mark that submit was attempted during email check
                sessionStorage.setItem('emailCheckTriggeredBySubmit', 'true');

                // Trigger email check if not already in progress
                if (!emailField.classList.contains('checking-email')) {
                    emailField.classList.add('checking-email');
                    checkEmailFallback({currentTarget: emailField});
                }

                return false;
            });
        }

        //showLoadingMessageFallback(emailField);

        try {
            const response = await fetch('/event/check_email_portal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: { email: email },
                    id: Math.floor(Math.random() * 1000000)
                })
            });

            const data = await response.json();
            const result = data.result || {};
            console.log("result.has_account", result.has_account);

            if (result.has_account) {
                console.log('✅ FALLBACK: Email HAS account - KEEPING SUBMIT BLOCKED');
                showPortalMessageFallback(emailField, true);
                hideSubmitButtonFallback('This email already has a portal account.');
                // Keep the form blocked - don't remove the submit.emailcheck handler
                sessionStorage.removeItem('emailCheckTriggeredBySubmit');
            } else {
                console.log('✅ FALLBACK: Email does NOT have account - UNBLOCKING SUBMIT');
                // Unblock the form since email is available
                form.off('submit.emailcheck');

                // If this check was triggered by a submit attempt, submit the form now
                if (isSubmitTriggered) {
                    console.log('🚀 Auto-submitting form after email validation');
                    sessionStorage.removeItem('emailCheckTriggeredBySubmit');

                    // Small delay to ensure DOM is ready
                    setTimeout(() => {
                        form[0].submit(); // Use native submit to avoid triggering our handler
                    }, 100);
                }
            }

        } catch (error) {
            console.error('❌ FALLBACK: Error:', error);
            showPortalMessageFallback(emailField, null, 'Error checking email');
            hideSubmitButtonFallback('Email validation failed');
            sessionStorage.removeItem('emailCheckTriggeredBySubmit');
        } finally {
            // Remove checking state
            emailField.classList.remove('checking-email');
        }
    }

    function hideSubmitButtonFallback(message) {
        console.log('🚫 FALLBACK: Hiding submit button');

        const submitButton = $('.js_submit_button');
        const form = submitButton.closest('form');

        if (submitButton.length > 0) {
            submitButton.hide().prop('disabled', true);

            // Avoid adding duplicate messages
//            if (!form.find('.submit-blocked-message').length) {
//                submitButton.after(`
//                    <div class="submit-blocked-message alert alert-danger mt-2">
//                        <strong><i class="fa fa-ban"></i> Registration Blocked:</strong> ${message}
//                    </div>
//                `);
//            }

            form.off('submit.emailcheck').on('submit.emailcheck', function(e) {
                e.preventDefault();
                e.stopPropagation();
                alert('Registration is not allowed for this email address.');
                return false;
            });
        } else {
            console.log('⚠️ Submit button not found.');
        }
    }

    function showSubmitButtonFallback() {
        console.log('✅ FALLBACK: Showing submit button');

        const form = $('form').first();
        const submitButton = form.find('button[type="submit"], input[type="submit"]');

        if (submitButton.length > 0) {
            submitButton.show();
            submitButton.prop('disabled', false);
            form.find('.submit-blocked-message').remove();
            form.off('submit.emailcheck');
        }
    }

    // Helper functions
    function isValidEmailFallback(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function showLoadingMessageFallback(element) {
        clearPortalMessageFallback(element);
        $(element).after(`
            <div class="portal-message text-muted small mt-1">
                <i class="fa fa-spinner fa-spin"></i> Checking email...
            </div>
        `);
    }

    function showPortalMessageFallback(element, hasAccount, errorMessage = null) {
        clearPortalMessageFallback(element);

        let message, alertClass;
        if (errorMessage) {
            message = `<i class="fa fa-exclamation-triangle"></i> ${errorMessage}`;
            alertClass = 'alert alert-danger';
        } else if (hasAccount) {
            message = `<i class="fa fa-ban"></i> This email already has a portal account!`;
            alertClass = 'alert alert-warning';
        } else {
            message = `<i class="fa fa-check-circle"></i> Email is available for registration.`;
            alertClass = 'alert alert-success';
        }

        $(element).after(`
            <div class="portal-message mt-2 mb-2">
                <div class="${alertClass} py-2 px-3 small">${message}</div>
            </div>
        `);
    }

    function clearPortalMessageFallback(element) {
        $(element).next('.portal-message').remove();
    }
});

export default publicWidget.registry.EventEmailPortalCheck;
