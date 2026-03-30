"""Geometry primitives for artifact rendering.

Canonical primitive types consumed by all renderers.
Primitives are pure geometry — no rendering logic, no classification.

Supported primitives:
    LINE, ARC, POLYLINE, RECTANGLE, TEXT, HATCH, DIMENSION, CALLOUT
"""

from dataclasses import dataclass, field
from typing import Any
import math


SUPPORTED_PRIMITIVES = frozenset({
    "LINE", "ARC", "POLYLINE", "RECTANGLE",
    "TEXT", "HATCH", "DIMENSION", "CALLOUT",
})


@dataclass(frozen=True)
class Point2D:
    """Immutable 2D point in drawing units (inches)."""
    x: float = 0.0
    y: float = 0.0

    def distance_to(self, other: "Point2D") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def to_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)


@dataclass
class LinePrimitive:
    """A line segment between two points."""
    primitive_type: str = "LINE"
    start: Point2D = field(default_factory=Point2D)
    end: Point2D = field(default_factory=Point2D)
    layer: str = ""
    lineweight: float = 0.25

    def length(self) -> float:
        return self.start.distance_to(self.end)


@dataclass
class ArcPrimitive:
    """A circular arc defined by center, radius, and angles."""
    primitive_type: str = "ARC"
    center: Point2D = field(default_factory=Point2D)
    radius: float = 1.0
    start_angle: float = 0.0
    end_angle: float = 360.0
    layer: str = ""
    lineweight: float = 0.25

    def sweep_angle(self) -> float:
        sweep = self.end_angle - self.start_angle
        if sweep < 0:
            sweep += 360.0
        return sweep

    def is_full_circle(self) -> bool:
        return abs(self.sweep_angle() - 360.0) < 0.001


@dataclass
class PolylinePrimitive:
    """A polyline defined by ordered vertices."""
    primitive_type: str = "POLYLINE"
    points: list[Point2D] = field(default_factory=list)
    closed: bool = False
    layer: str = ""
    lineweight: float = 0.25

    def vertex_count(self) -> int:
        return len(self.points)

    def segment_count(self) -> int:
        if len(self.points) < 2:
            return 0
        return len(self.points) if self.closed else len(self.points) - 1


@dataclass
class RectanglePrimitive:
    """An axis-aligned rectangle."""
    primitive_type: str = "RECTANGLE"
    origin: Point2D = field(default_factory=Point2D)
    width: float = 0.0
    height: float = 0.0
    layer: str = ""
    lineweight: float = 0.25

    def area(self) -> float:
        return abs(self.width * self.height)

    def corners(self) -> list[Point2D]:
        x, y = self.origin.x, self.origin.y
        return [
            Point2D(x, y),
            Point2D(x + self.width, y),
            Point2D(x + self.width, y + self.height),
            Point2D(x, y + self.height),
        ]


@dataclass
class TextPrimitive:
    """A text element at a given position."""
    primitive_type: str = "TEXT"
    text: str = ""
    position: Point2D = field(default_factory=Point2D)
    height: float = 0.125
    rotation: float = 0.0
    layer: str = ""
    font: str = "standard"
    alignment: str = "left"


@dataclass
class HatchPrimitive:
    """A hatch fill pattern within a boundary."""
    primitive_type: str = "HATCH"
    boundary: list[Point2D] = field(default_factory=list)
    pattern: str = "ANSI31"
    scale: float = 1.0
    angle: float = 0.0
    layer: str = ""

    def boundary_vertex_count(self) -> int:
        return len(self.boundary)


@dataclass
class DimensionPrimitive:
    """A dimension annotation between two points."""
    primitive_type: str = "DIMENSION"
    start: Point2D = field(default_factory=Point2D)
    end: Point2D = field(default_factory=Point2D)
    offset: float = 0.5
    text: str = ""
    unit: str = "in"
    layer: str = ""
    precision: int = 2

    def measured_value(self) -> float:
        return self.start.distance_to(self.end)


@dataclass
class CalloutPrimitive:
    """A callout bubble with leader line."""
    primitive_type: str = "CALLOUT"
    anchor: Point2D = field(default_factory=Point2D)
    leader_end: Point2D = field(default_factory=Point2D)
    text: str = ""
    bubble_radius: float = 0.25
    layer: str = ""


# Type alias for any primitive
Primitive = (
    LinePrimitive | ArcPrimitive | PolylinePrimitive | RectanglePrimitive |
    TextPrimitive | HatchPrimitive | DimensionPrimitive | CalloutPrimitive
)


def get_primitive_type(primitive: Primitive) -> str:
    """Return the primitive type string."""
    return primitive.primitive_type


def validate_primitive(primitive: Primitive) -> list[str]:
    """Validate a primitive for rendering readiness. Returns list of errors."""
    errors = []

    if not hasattr(primitive, "primitive_type"):
        errors.append("Primitive missing primitive_type attribute.")
        return errors

    if primitive.primitive_type not in SUPPORTED_PRIMITIVES:
        errors.append(f"Unsupported primitive type: '{primitive.primitive_type}'.")

    if not primitive.layer:
        errors.append(f"Primitive '{primitive.primitive_type}' has no layer assigned.")

    if isinstance(primitive, LinePrimitive):
        if primitive.start == primitive.end:
            errors.append("LINE primitive has zero length (start == end).")

    if isinstance(primitive, ArcPrimitive):
        if primitive.radius <= 0:
            errors.append(f"ARC primitive has non-positive radius: {primitive.radius}.")

    if isinstance(primitive, PolylinePrimitive):
        if len(primitive.points) < 2:
            errors.append(f"POLYLINE has fewer than 2 points: {len(primitive.points)}.")

    if isinstance(primitive, RectanglePrimitive):
        if primitive.width <= 0 or primitive.height <= 0:
            errors.append(f"RECTANGLE has non-positive dimensions: {primitive.width}x{primitive.height}.")

    if isinstance(primitive, TextPrimitive):
        if not primitive.text:
            errors.append("TEXT primitive has empty text.")

    if isinstance(primitive, HatchPrimitive):
        if len(primitive.boundary) < 3:
            errors.append(f"HATCH boundary has fewer than 3 points: {len(primitive.boundary)}.")

    if isinstance(primitive, DimensionPrimitive):
        if primitive.start == primitive.end:
            errors.append("DIMENSION primitive has zero length (start == end).")

    if isinstance(primitive, CalloutPrimitive):
        if not primitive.text:
            errors.append("CALLOUT primitive has empty text.")

    return errors
