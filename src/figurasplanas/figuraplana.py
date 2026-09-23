from math import pi, sqrt, sin, cos, atan


class FiguraPlana:
    """Representa uma figura plana genérica por suas propriedades geométricas.

    A classe armazena a área, os momentos de inércia em relação aos
    eixos x e y, o produto de inércia Ixy, e a posição do centroide (xc, yc).
    A partir desses dados, ela calcula também os momentos principais, o ângulo
    principal theta_p e os raios de giração associados.

    obs:
     - I1 é o momento de inércia principal central máximo
     - theta_p é o ângulo entre o eixo x e o eixo principal central 1 ( - pi/2 < theta_p <= pi/2 )

    Atributos:
        A (float): área.
        Ix (float): momento de inércia em relação ao eixo x global.
        Iy (float): momento de inércia em relação ao eixo y global.
        Ixy (float): produto de inércia da seção em relação aos eixos x e y.
        xc (float): coordenada x do centroide.
        yc (float): coordenada y do centroide.
        Io (float): momento polar de inércia para origem dos eixos x-y.
        Sx, Sy (float): momentos estáticos em relação aos eixos x e y.
        rx, ry (float): raios de giração em relação aos eixos x e y.
        ro (float): raio de giração polar para origem dos eixos x-y.
        Ic (float): momento de inércia polar em relação ao centroide.
        I1, I2 (float): momentos principais de inércia (I1 >= I2).
        theta_p (float): ângulo entre o eixo x e o eixo principal 1 .
        r1, r2 (float): raios de giração principais.

    Métodos:
        transladar(xc, yc): atualiza a posição do centroide e recalcula as
            propriedades.
        rotacionar(theta_p): redefine o ângulo dos eixos principais e recalcula
            as propriedades.
    """
    
    def __init__(self, A:float, Ix:float, Iy:float, xc:float, yc:float, Ixy:float)-> None: 
        self.A = A
        self.Ix = Ix
        self.Iy = Iy
        self.Ixy = Ixy
        self.xc = xc
        self.yc = yc

        if any([value < 0 for value in [A, Ix, Iy]]):
            raise ValueError("Área e momentos de inércia devem ser não-negativos.")
        if Ix*Iy < Ixy**2:
            raise ValueError("Há inconsistência nos valores de Ix, Iy, Ixy.")
        
        self._eixos_principais_centrais()
        self._calcular_propriedades(update=False)


    def _eixos_principais_centrais(self) -> None:
        self.Ix_a = self.Ix - self.yc**2 * self.A
        self.Iy_a = self.Iy - self.xc**2 * self.A
        self.Ixy_a = self.Ixy - self.xc * self.yc * self.A

        Im = (self.Ix_a + self.Iy_a) / 2
        Id = (self.Ix_a - self.Iy_a) / 2
        Ir = sqrt( Id**2 + self.Ixy_a**2 )

        self.I1 = Im + Ir
        self.I2 = Im - Ir
        if Id != 0:
            self.theta_p = 0.5 * atan(self.Ixy_a / Id)
        elif self.Ixy_a ==0:
            self.theta_p = pi
        else:
            self.theta_p = pi/4 if self.Ixy_a > 0 else -pi/4

        if self.I2 <=0:
            raise ValueError("Há inconsistência nos valores de Ix, Iy, Ixy que resultam em I mínimo negativo.")

        #reverte a consideração incial de que Imax está próximo de Ix_a
        if abs(self.theta_p) < pi/4 and self.Ix_a < self.Iy_a:
            self.theta_p = self.theta_p + pi/2 if self.theta_p < 0 else self.theta_p - pi/2
       
        self.r1 = sqrt( self.I1 / self.A )
        self.r2 = sqrt( self.I2 / self.A )
        self.Ic = self.I1 + self.I2


    def _calcular_propriedades(self,update:bool) -> None:

        if update:
            self.Ix = self.Ix_a + self.yc**2 * self.A
            self.Iy = self.Iy_a + self.xc**2 * self.A
            self.Ixy = self.Ixy_a + self.xc * self.yc * self.A

        self.Io = self.Ix + self.Iy
        self.Sx = self.xc * self.A
        self.Sy = self.yc * self.A
        self.rx = sqrt( self.Ix / self.A )
        self.ry = sqrt( self.Iy / self.A )
        self.ro = sqrt( self.Io / self.A )




    def transladar(self, dx:float, dy:float) -> None:
        """Translada a figura plana com deslocamento (dx, dy)."""
        self.xc = self.xc + dx
        self.yc = self.yc + dy
        self._calcular_propriedades(update=True)


    def rotacionar(self, ang:float) -> None:
        """
        Rotação de um ângulo `ang` em torno da origem do sistema de coordenadas.
        Obs.: ang em radianos e positivo no sentido anti-horário
        """

        s2 = sin(-2 * ang)
        c2 = cos(-2 * ang)
        Im = (self.Ix + self.Iy) / 2
        Id = (self.Ix - self.Iy) / 2
        Iv = Id * c2 + self.Ixy * s2

        Ix  = Im + Iv
        Iy  = Im - Iv
        Ixy = Id * s2 + self.Ixy * c2

        xc = self.xc * cos(-ang) - self.yc * sin(-ang)
        yc = self.xc * sin(-ang) + self.yc * cos(-ang)

        self.Ix = Ix
        self.Iy = Iy
        self.Ixy = Ixy
        self.xc = xc
        self.yc = yc

        self._eixos_principais_centrais()
        self._calcular_propriedades(update=True)

    def ajustar_posição(self, xc:float, yc:float, theta_p:float):

        self.xc = xc
        self.yc = yc

        self.theta_p = ( (theta_p + pi/2) % pi ) - pi/2

        s2 = sin(-2 * self.theta_p)
        c2 = cos(-2 * self.theta_p)
        Im = (self.I1 + self.I2) / 2
        Ir = (self.I1 - self.I2) / 2
        self.Ix_a  = Im + Ir * c2
        self.Iy_a  = Im - Ir * c2
        self.Ixy_a = Ir * s2

        self._calcular_propriedades(update=True)

    def __repr__(self) -> str:
        return f"FiguraPlana(A={self.A}, Ix={self.Ix}, Iy={self.Iy}, Ixy={self.Ixy}, xc={self.xc}, yc={self.yc})"
    
    def __str__(self) -> str:
        def formatar_linha(*propriedades: tuple[str, float]) -> str:
            return ", ".join(
                f"{nome:>7}: {valor:>12.4e}"
                for nome, valor in propriedades
            )

        return (
            formatar_linha(
                ("A", self.A), ("Ix", self.Ix), ("Iy", self.Iy),
                ("Ixy", self.Ixy), ("xc", self.xc), ("yc", self.yc),
            ) + "\n" +
            formatar_linha(
                ("Io", self.Io), ("Sx", self.Sx), ("Sy", self.Sy),
                ("rx", self.rx), ("ry", self.ry), ("ro", self.ro),
            ) + "\n" +
            formatar_linha(
                ("I1", self.I1), ("I2", self.I2),
                ("theta_p", self.theta_p), ("Ic", self.Ic),
                ("r1", self.r1), ("r2", self.r2),
            )
        )