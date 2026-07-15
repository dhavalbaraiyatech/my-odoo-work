# Website Sale - Default Shipping Address

Lets a customer mark one of their delivery addresses as the **default shipping
address**, so it gets pre-selected automatically on future website orders
instead of having to be picked manually every time.

## Functionality

- Adds a boolean field `is_default_shipping_address` on `res.partner`.
- Adds a **"Set as default shipping address" / "Remove default shipping
  address"** button on every delivery address card, on:
  - the shop checkout page (`/shop/checkout`)
  - the portal address list page (`/my/addresses`)

  The button only appears on **delivery** addresses (not billing), right next
  to the existing "Edit" action on the card, and toggles between "Set as
  default" and "Remove default" depending on the address's current state.
- Only one address per customer (per commercial partner / company) can be the
  default at a time. Setting a new default — whether by clicking the button,
  through the backend `res.partner` form, or via any other write to the
  field — automatically clears the flag from any other address in the same
  customer family.
- When a product is added to the cart, the order's shipping address
  (`partner_shipping_id`) is automatically set to the customer's default
  address, if one is defined.
- Clicking the button on the checkout page also immediately updates the
  shipping address of the current cart, if one is open.
- The `is_default_shipping_address` field is also visible and editable
  directly on the contact/address form in the backend (`Settings > Users &
  Companies > Contacts`, or the "Addresses" tab of a customer), restricted to
  `delivery`, `other`, and `contact` type addresses.

## How it works

| Layer | File | Purpose |
|---|---|---|
| Model | `models/res_partner.py` | `is_default_shipping_address` field; enforces the "only one default per commercial partner" rule on `write`/`create`; helper methods to set/unset the default. |
| Model | `models/sale_order.py` | Auto-assigns the customer's default shipping address to the order when a product is first added to the cart. |
| Controller | `controllers/main.py` | JSON-RPC routes `/shop/set_default_shipping_address` and `/shop/unset_default_shipping_address`, called from the frontend button. Restricted to addresses belonging to the logged-in user's own customer family. |
| Views | `views/res_partner_views.xml` | Exposes the field on the backend contact form. |
| Views | `views/website_sale_default_address_templates.xml` | Injects the button (and, optionally, a "Default" badge) into the address card template used by checkout (`website_sale.address_card`) and by the portal address list (`portal.address_card`). |
| Frontend | `static/src/js/default_address.js` | Website `Interaction` that wires up the button clicks to the JSON-RPC routes and reloads the page to reflect the change. |
| Frontend | `static/src/css/default_address.css` | Minor styling for the button/badge. |

## Usage

1. Go to `/shop/checkout` or `/my/addresses` while logged in.
2. Under a delivery address, click **"Set as default shipping address"**.
3. The address is now the default: the button changes to **"Default Shipping
   Address"** (click again to remove the default), and any other address
   previously marked as default is automatically un-marked.
4. On the next order, that address is pre-selected as the shipping address.

## Dependencies

- `website_sale`

## Notes / limitations

- The default-address logic is scoped per **commercial partner** (i.e. a
  company and its child contacts share the same "one default" pool), matching
  how Odoo groups a customer's delivery addresses.
- No dedicated backend menu/view is added for reporting on default addresses;
  the field is only exposed on the existing contact form.