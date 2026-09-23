from math import sin, cos
from .figura_simples import *


class FiguraComposta(FiguraPlana):
 
    def __init__(self) -> None:
        self.partes = []
        self.coef = []


    def __len__(self) -> int:
        return len(self.partes)

    def adiciona(self, figura:FiguraPlana, coef=1.0) -> None:
        self.partes.append(figura)
        self.coef.append(coef)
        self._calcular_propriedades_secao_composta()

    def remove(self, i: int) -> None:
        if 0 <= i < len(self.partes):
            del self.partes[i]
            del self.coef[i]
            self._calcular_propriedades_secao_composta()

    def _calcular_propriedades_secao_composta(self) -> None:

        A = Sx = Sy = Ix = Iy = Ixy = 0.0
        for fig, c in zip(self.partes, self.coef):
            A += c * fig.A
            Sx += c * fig.Sx
            Sy += c * fig.Sy
            Ix += c * fig.Ix
            Iy += c * fig.Iy
            Ixy += c * fig.Ixy

        xc = Sx / A if A != 0 else 0.0
        yc = Sy / A if A != 0 else 0.0

        self.A = A
        self.xc = xc
        self.yc = yc
        self.Ix = Ix
        self.Iy = Iy
        self.Ixy = Ixy

        self._eixos_principais_centrais()
        self._calcular_propriedades(update=False)


    def transladar(self, dx:float, dy:float) -> None:
        for fig in self.partes:
            fig.transladar(dx, dy)

        self._calcular_propriedades_secao_composta()

    def rotacionar(self, ang:float) -> None:
        for fig in self.partes:
            fig.rotacionar(ang)

        self._calcular_propriedades_secao_composta()

    def __repr__(self) -> str:
        return f"FiguraComposta(partes={self.partes.__repr__()})"

    def __str__(self) -> str:
        txt = f"Figura Composta: {len(self.partes)} partes\n"
        if len(self.partes) > 0:
            for i, fig in enumerate(self.partes):
                txt += f"  {i}: {fig.__repr__()}\n"
            txt += super().__str__()
        return txt