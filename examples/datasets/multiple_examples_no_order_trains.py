from typing import List
from examples.datasets.data.train_example_data import train_example_data

from neuralogic.core import Relation, Template, Var, Constant
from neuralogic.dataset import Dataset


dataset = Dataset()

template = Template()

# One example per train, doesn't know order of vagons

# fmt: off

shapes = [Constant.ellipse, Constant.rectangle, Constant.bucket, Constant.hexagon, Constant.u_shaped]
roofs = [Constant.jagged, Constant.arc, Constant.none, Constant.flat, Constant.peaked]
loadshapes = [Constant.hexagon, Constant.triangle, Constant.diamond, Constant.rectangle, Constant.circle]
vagon_atoms = [Relation.shape, Relation.length, Relation.sides, Relation.wheels, Relation.loadnum, Relation.loadshape, Relation.roof]

Y = Var.Y   #todo gusta: tohle je dobry trik, ten bych pouzival na vic mistech, a podobne pro Atom/Predicate factories udelat zkratky (treba P.)

template.add_rules(
    [
        *[Relation.shape(Y) <= Relation.shape(Y, s)[1,] for s in shapes],
        *[Relation.length(Y) <= Relation.length(Y, s)[1,] for s in [Constant.short, Constant.long]],
        *[Relation.sides(Y) <= Relation.sides(Y, s)[1,] for s in [Constant.not_double, Constant.double]],
        *[Relation.roof(Y) <= Relation.roof(Y, s)[1,] for s in roofs],
        *[Relation.wheels(Y) <= Relation.wheels(Y, s)[1,] for s in [2, 3]],
        *[Relation.loadnum(Y) <= Relation.loadnum(Y, s)[1,] for s in [0, 1, 2, 3]],
        *[Relation.loadshape(Y) <= Relation.loadshape(Y, s)[1,] for s in loadshapes],
        Relation.vagon(Y) <= (atom(Y)[1,] for atom in vagon_atoms),
        Relation.train <= Relation.vagon(Y)[1,],
        Relation.direction <= Relation.train[1,],
    ]
)

examples: List[List] = [[]] * 20

for _, id, pos, shape, length, sides, roof, wheels, load, loadnum in train_example_data:
    if not examples[id - 1]:
        examples[id - 1] = []
    examples[id - 1].extend(
        [
            Relation.shape(pos, shape),
            Relation.length(pos, length),
            Relation.sides(pos, sides),
            Relation.roof(pos, roof),
            Relation.wheels(pos, wheels),
            Relation.loadshape(pos, load),
            Relation.loadnum(pos, loadnum),
        ]
    )

dataset.add_examples(examples)
dataset.add_queries([*[Relation.direction[1.0] for _ in range(1, 11)], *[Relation.direction[-1.0] for _ in range(11, 21)]])
