# 05_RENDER_ENGINE.md

Version: 1.0

Status: CANONICAL

Pack: 05

Engine: Report Engine

Component: Render Engine

---

# 1. Purpose

The Render Engine transforms a themed LayoutTree into a platform-neutral RenderTree.

The RenderTree is the canonical visual representation of the report.

The Render Engine never performs layout construction.

The Render Engine never exports documents.

The Render Engine never modifies interpretation content.

---

# 2. Position in Runtime

InterpretationResult

↓

Presentation Context

↓

Report Layout Engine

↓

LayoutTree

↓

Theme Engine

↓

ThemedLayoutTree

↓

Render Engine

↓

RenderTree

↓

Export Engine

↓

ReportResult

---

# 3. Rendering Philosophy

Rendering transforms presentation structure into renderable objects.

Rendering never changes

- narrative
- layout
- theme
- business meaning

Rendering prepares objects for downstream renderers.

---

# 4. Responsibilities

The Render Engine is responsible for

✓ Render Node Construction

✓ Render Hierarchy

✓ Render Constraints

✓ Responsive Render Rules

✓ Render Metadata

✓ Render Optimization

The Render Engine is NOT responsible for

✗ Layout

✗ Theme

✗ PDF

✗ HTML

✗ React

✗ Flutter

✗ Export

---

# 5. Runtime Flow

ThemedLayoutTree

↓

Render Node Builder

↓

Container Builder

↓

Text Builder

↓

Media Builder

↓

Render Validation

↓

RenderTree

---

# 6. Input

Consumes

ThemedLayoutTree

Containing

Layout

Theme

Typography

Spacing

Assets

Navigation

Metadata

---

# 7. Output

Produces

RenderTree

RenderTree is immutable.

RenderTree is platform neutral.

---

# 8. Render Tree

Hierarchy

Document

↓

Render Page

↓

Render Section

↓

Render Container

↓

Render Element

↓

Render Content

Every Render Node represents one visual object.

---

# 9. Render Node

Every Render Node contains

Render ID

Node Type

Bounds

Layout Constraints

Style

Children

Metadata

Trace

---

# 10. Render Containers

Supported containers

Page

Section

Card

Grid

Stack

Row

Column

Group

Containers organize visual elements.

---

# 11. Render Elements

Supported elements

Heading

Paragraph

Label

Value

Image

Table

Chart

Divider

Icon

Badge

Elements remain presentation only.

---

# 12. Responsive Rendering

Supported profiles

Desktop

Laptop

Tablet

Mobile

Print

Only rendering adapts.

LayoutTree remains unchanged.

---

# 13. Render Constraints

Supported constraints

Width

Height

Min Width

Max Width

Alignment

Spacing

Overflow

Visibility

Constraints are immutable.

---

# 14. Style Resolution

Resolved styles include

Typography

Spacing

Borders

Radius

Elevation

Color Tokens

Icon Tokens

Render Engine never creates themes.

---

# 15. Asset Resolution

Resolve

Icons

SVG

Charts

Fonts

Illustrations

Images

Assets are referenced only.

---

# 16. Render Metadata

Every Render Node stores

Node ID

Layout ID

Theme ID

Render Order

Trace ID

Metadata

Supports debugging.

---

# 17. Validation

Validate

✓ Render Tree

✓ Constraints

✓ Styles

✓ Assets

✓ References

✓ Navigation

No invalid Render Node is allowed.

---

# 18. Error Handling

Possible errors

RenderNodeError

StyleError

ConstraintError

AssetError

ValidationError

RuntimeError

Errors return

Result.Error

---

# 19. Performance

Target

1,000 Render Nodes

↓

RenderTree

<30 ms

Supports parallel rendering.

---

# 20. Thread Safety

The Render Engine is

✓ Stateless

✓ Immutable

✓ Deterministic

✓ Thread-safe

---

# 21. Downstream Contract

Produces

RenderTree

Consumed by

Desktop Renderer

Mobile Renderer

PDF Renderer

Print Renderer

Future Renderers

No renderer rebuilds RenderTree.

---

# 22. Acceptance Criteria

The Render Engine is complete when

✓ Render Tree created

✓ Render Nodes created

✓ Containers created

✓ Elements created

✓ Constraints resolved

✓ Styles resolved

✓ Validation passed

✓ Thread-safe

✓ Deterministic

✓ Performance targets achieved

✓ Documentation approved

---

END OF DOCUMENT