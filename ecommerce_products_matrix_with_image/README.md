# b2b_ecommerce_matrix

Odoo 19 module providing a B2B product variant matrix and related controls.

Install as a normal Odoo addon. Configure freight rules and MOV from the B2B > Configurations menu.

Front-end: product page will render a matrix when user is logged in and product has Size/Color attributes.

Testing: run Odoo tests: `odoo-bin -c <conf> -d <db> --test-enable --stop-after-init -i b2b_ecommerce_matrix`
