# ARCHITECTURE

## Boundary

| Owns | Does not own |
|------|----------------|
| Life stage / reader / package | Engine facts |
| Feature visibility | CDR relations |
| Language/action profile selection | Claim truth |
| Audience delivery wrappers | CLL writing standard source |

## Flow

1. Truth composition (unchanged)  
2. `ProductContextEngine.resolve(ProductContextInput)`  
3. `ContextDeliveryAdapter.apply` — pass-through for adults; child/parent adaptation  
4. Customer deliverable + report sections  

Adult SELF default = **pass_through** (CASE-0001 / CASE-0002 bodies unchanged).
