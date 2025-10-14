==============
Invoice Email Connector
==============

.. 


.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3


|badge1| |badge2|

This module adds additional features required for accounting.
When a user generates an invoice or bill and wants to send it to another lead or system by email,
the standard model does not provide this functionality.

Our module offers the solution by providing new fields, buttons, and extended features.


**Table of contents**

.. contents::
   :local:

Configuration
=============

A button **Send to Multiple emails** is available.
It can be configured by going to *Configuration > Settings* and enabling *Enable email Integration*.
This allows you to add email addresses to journals.

To send the email to a specific address, you must fill in the **Email** field in the journal.


Usage
=====

The concept of this module is to send emails directly to Multiple emails.
Emails expects to receive emails containing invoices, bills, and miscellaneous entries.

After configuring the journal and filling in the **Emails** email field,
each flow can automatically send the corresponding documents by email:

1. Invoice.
   Customers > Invoice
   Button "Send" opens a popup
   Enable the field email

2. **Bill**
   - Path: *Vendors > Bills*
   - Action: Click the **Send to Multiple emails** button.
   - Behavior: The button is only visible if attachments exist.

3. **Miscellaneous**
   - Path: *Accounting > Miscellaneous*
   - Action: Click the **Send to Multiple emails** button.
   - Behavior: The button is only visible if attachments exist.



Maintainers
-----------

This module is maintained by the ElaviAgency.



