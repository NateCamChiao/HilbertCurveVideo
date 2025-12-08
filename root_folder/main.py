from manim import *
import numpy as np
from PIL import Image as PILImage
from io import BytesIO
class DefaultTemplate(MovingCameraScene):
    def split_map_image(self, filename="HilbertMap.png", rows=4, cols=4, save_crops=False):
        pil = PILImage.open(filename).convert("RGBA")
        w, h = pil.size
        side = min(w, h)
        # center-crop to square
        left = (w - side) // 2
        top = (h - side) // 2
        pil = pil.crop((left, top, left + side, top + side))

        tile_w = side // cols
        tile_h = side // rows

        tiles = []
        for r in range(rows):
            for c in range(cols):
                box = (c * tile_w, r * tile_h, (c + 1) * tile_w, (r + 1) * tile_h)
                crop = pil.crop(box)
                if save_crops:
                    crop.save(f"crop_{r}_{c}.png")
                arr = np.array(crop)  # convert to numpy array for ImageMobject
                tiles.append(ImageMobject(arr))

        grid = Group(*tiles).arrange_in_grid(rows, cols, buff=0).move_to(ORIGIN)
        return grid
    def getHilbertPoints(self, order, startPoint, step):
        def generatePoints(steps, order):
            if order <= 1:
                return steps
            newString = []
            A = "+BF-AFA-FB+"
            B = "-AF+BFB+FA-"

            for char in steps:
                if char == "A":
                    newString += A
                elif char == "B":
                    newString += B
                else:
                    newString += char
            return generatePoints(newString, order - 1)
        def getCoordinates(instructions, pointsArray, stepSize):
            direction = 0  # 0: right, 1: up, 2: left, 3: down
            for char in instructions:
                if char == "F":
                    if direction == 0:
                        pointsArray.append([pointsArray[-1][0] + stepSize, pointsArray[-1][1], 0])
                    elif direction == 1:
                        pointsArray.append([pointsArray[-1][0], pointsArray[-1][1] + stepSize, 0])
                    elif direction == 2:
                        pointsArray.append([pointsArray[-1][0] - stepSize, pointsArray[-1][1], 0])
                    elif direction == 3:
                        pointsArray.append([pointsArray[-1][0], pointsArray[-1][1] - stepSize, 0])
                elif char == "+":
                    direction = (direction + 1) % 4
                elif char == "-":
                    direction = (direction - 1) % 4
            return pointsArray

        return getCoordinates(generatePoints("+BF-AFA-FB+", order), [startPoint], step)
    def intro(self):
        square = Rectangle(width=8, height=5, color=WHITE).to_edge(UP)
        path = VMobject()
        path.set_points_as_corners([LEFT, UP, RIGHT, DOWN, LEFT])
        path.set
        title = Text("The Hilbert Curve", font_size=42, weight=BOLD).move_to(square.get_center() + 0.5 * UP)
        name = Text("By: Nate Cameron-Chiao", font_size=30).next_to(title, DOWN * 2)
        self.play(
            Create(square).set_run_time(2),
            Write(title),
            Write(name)
        )
        self.wait(1)
        self.play(
            title.animate.move_to(UP * 7),
            name.animate.move_to(UP * 7),
            square.animate.move_to(UP * 7)
        )
    def tableOfContents(self):
        self.tableOfContents = Text("Table of Contents", font_size=36, weight=BOLD).move_to(ORIGIN + UP * 1.8)
        line1 = Text("1. History", font_size=28).next_to(self.tableOfContents, DOWN * 2)
        line2 = Text("2. Construction", font_size=28).next_to(line1, DOWN)
        line3 = Text("3. Applications", font_size=28).next_to(line2, DOWN)
        # line4 = Text("4. Conclusion", font_size=28).next_to(line3, DOWN)
        self.tableOfContentsGroup = VGroup(self.tableOfContents, line1, line2, line3).arrange(DOWN, center=False, aligned_edge=LEFT)
        self.play(Write(self.tableOfContentsGroup).set_run_time(2))
        self.wait(5)
    
    def hilbertHistory(self):
        hilbertImage = ImageMobject("Hilbert.png").move_to(LEFT * 12)
        hilbertLabel = Text("David Hilbert", font_size=24).next_to(hilbertImage, DOWN)
        self.add(hilbertImage, hilbertLabel)
        self.play(
            self.tableOfContentsGroup.animate.to_edge(LEFT).scale(0.3).shift(UP * 5),
            hilbertImage.animate.move_to(ORIGIN)
        )
        self.play(hilbertLabel.animate.next_to(hilbertImage, DOWN))
        
        self.wait()

        self.play(FadeOut(hilbertLabel), FadeOut(hilbertImage))
        # animate rectangle filling from the bottom to the top
        line = VMobject()
        line.set_points_as_corners([[-4, -2.5, 0], [3, -2.5, 0]]).move_to(ORIGIN)
        curve = VMobject()
        curve.set_points_as_corners(self.getHilbertPoints(3, [-4, -2.5, 0], 0.4125)).move_to(ORIGIN)
        line.set_color(color_gradient([RED, ORANGE, YELLOW, GREEN], line.get_num_points()))
        curve.set_color(color_gradient([RED, ORANGE, YELLOW, GREEN], curve.get_num_points()))
        higherOrderCurve = VMobject()
        higherOrderCurve.set_points_as_corners(self.getHilbertPoints(4, [-4, -2.5, 0], 0.20625)).move_to(ORIGIN)
        higherOrderCurve.set_color(color_gradient([RED, ORANGE, YELLOW, GREEN], higherOrderCurve.get_num_points())).move_to(ORIGIN)

        frame = Square(side_length=curve.get_width()+0.3, color=WHITE).move_to(ORIGIN)
        self.play(
            Create(line).set_run_time(2)
        )
        
        self.play(
            Transform(line, curve).set_run_time(6)
        )
        self.wait(1)

        hilbertCurveFunctionLabel = Text("lim   f  (x)", font_size=30).to_edge(LEFT)
        subScript = Text("n", font_size=20).next_to(hilbertCurveFunctionLabel, RIGHT, buff=0.1).shift(DOWN * 0.2 + LEFT * 0.75)

        nLabel = Text("n → ∞", font_size=20).next_to(hilbertCurveFunctionLabel, DOWN, buff=0.1).shift(LEFT * 0.6)

        orderLabel = Text("(n is the order of the curve)", font_size=20).move_to(nLabel.get_center() + RIGHT + DOWN * 0.5)
        self.play(
            Transform(line, higherOrderCurve).set_run_time(2),
            FadeIn(frame),
            Write(hilbertCurveFunctionLabel),
            Write(subScript),
            Write(nLabel),
            Write(orderLabel)
        )
        self.play(
            ScaleInPlace(line, 0.5),
            frame.animate.scale(0.5)
        )
        spaceFilling = Text("Space-Filling Curve", font_size=30).to_edge(UP)
        crazyPoints = self.getHilbertPoints(5, [-4, -2.5, 0], 0.20625)
        highestOrderCurve = VMobject().set_points_as_corners(crazyPoints).move_to(ORIGIN)
        highestOrderCurve.set_color(color_gradient([RED, ORANGE, YELLOW, GREEN], highestOrderCurve.get_num_points())).move_to(ORIGIN).scale(0.25)
        self.play(Write(spaceFilling), Transform(line, highestOrderCurve))
        notDifferentiable = Text("Not differentiable", color = RED).move_to(DOWN * 2)

        self.wait(3)
        self.play(Create(notDifferentiable))   
        self.wait(5)

        self.play(
            FadeOut(line),
            FadeOut(frame),
            FadeOut(notDifferentiable),
            FadeOut(spaceFilling),  
            FadeOut(hilbertCurveFunctionLabel),
            FadeOut(subScript),
            FadeOut(nLabel),
            FadeOut(orderLabel)
        )

    def hilbertConstruction(self):
        hilbertCurveFrame = Rectangle(width=6, height=6, color=YELLOW).move_to(ORIGIN)
        grid = NumberPlane(x_range=[-3, 3, 3], y_range=[-3, 3, 3], background_line_style={"stroke_color": GREY, "stroke_width": 1}).move_to(ORIGIN)
        pointA = Dot(point=hilbertCurveFrame.get_corner(DL).__add__(-DL * 1.5), color=RED)
        pointALabel = Text("1", font_size=24).next_to(pointA, DOWN)
        pointB = Dot(point=hilbertCurveFrame.get_corner(UL).__add__(-UL * 1.5), color=RED)
        pointBLabel = Text("2", font_size=24).next_to(pointB, LEFT)
        pointC = Dot(point=hilbertCurveFrame.get_corner(UR).__add__(-UR * 1.5), color=RED)
        pointCLabel = Text("3", font_size=24).next_to(pointC, RIGHT)
        pointD = Dot(point=hilbertCurveFrame.get_corner(DR).__add__(-DR * 1.5), color=RED)
        pointDLabel = Text("4", font_size=24).next_to(pointD, DOWN)
        order1LabelGroup = VGroup(
                pointA, pointALabel,
                pointB, pointBLabel,
                pointC, pointCLabel,
                pointD, pointDLabel
        )
        self.play(
            Create(hilbertCurveFrame).set_run_time(2),
            Create(grid).set_run_time(2)
        )
        self.wait(1)
        self.play(
            LaggedStart(
                Create(pointA),
                Write(pointALabel),
                Create(pointB),
                Write(pointBLabel),
                Create(pointC),
                Write(pointCLabel), 
                Create(pointD),
                Write(pointDLabel),
                lag_ratio = 0.25
            )
        )
        connectedPath1 = VMobject()
        connectedPath1.set_points_as_corners([pointA.get_center(), pointB.get_center(), pointC.get_center(), pointD.get_center()])
        self.play(Create(connectedPath1), run_time=3)

        order1Lable = Text(" Order 1", font_size=30).to_edge(UP)
        self.play(Write(order1Lable))
        self.play(
            VGroup(
                pointA, pointALabel,
                pointB, pointBLabel,
                pointC, pointCLabel,
                pointD, pointDLabel,
                connectedPath1,
                order1Lable,
                grid,
                hilbertCurveFrame
            ).animate.scale(0.5).to_corner(DL),
        )
        self.wait(3)
        grid2 = NumberPlane(x_range=[-3, 3, 1.5], y_range=[-3, 3, 1.5], background_line_style={"stroke_color": GREY, "stroke_width": 1}).move_to(ORIGIN)
        frame2 = Rectangle(width=6, height=6, color=YELLOW).move_to(ORIGIN)
        order2Label = Text(" Order 2", font_size=30).to_edge(UP)
        self.play(
            Create(frame2),
            Create(grid2),
            Write(order2Label)
        )

        copiedOrder1DL = VGroup(connectedPath1.copy(), order1LabelGroup.copy())
        copiedOrder1UL = VGroup(connectedPath1.copy(), order1LabelGroup.copy())
        copiedOrder1UR = VGroup(connectedPath1.copy(), order1LabelGroup.copy())
        copiedOrder1DR = VGroup(connectedPath1.copy(), order1LabelGroup.copy())
        self.play(
            LaggedStart(
                copiedOrder1DL.animate.move_to(grid2.get_center() + DL * 1.5),
                copiedOrder1UL.animate.move_to(grid2.get_center() + UL * 1.5),
                copiedOrder1UR.animate.move_to(grid2.get_center() + UR * 1.5),
                copiedOrder1DR.animate.move_to(grid2.get_center() + DR * 1.5),
                lag_ratio=0.5
            )
        )
        self.wait(3)
        self.play(copiedOrder1DL.animate.rotate(-PI/2, about_point= copiedOrder1DL[0].get_center()))
        self.play(copiedOrder1DL.animate.apply_matrix([[1,0], [0, -1]], about_point = copiedOrder1DL.get_center()))
        
        self.play(copiedOrder1DR.animate.rotate(PI/2, about_point= copiedOrder1DR[0].get_center()))
        self.play(copiedOrder1DR.animate.apply_matrix([[1,0], [0, -1]], about_point = copiedOrder1DR.get_center()))

        order2Line = VMobject()
        order2Line.set_points_as_corners(
                copiedOrder1DL[0].get_all_points()    
        )
        order2Line.add_points_as_corners(
            copiedOrder1UL[0].get_all_points(),
        )
        order2Line.add_points_as_corners(
            copiedOrder1UR[0].get_all_points(),
        )
        order2Line.add_points_as_corners(
            copiedOrder1DR[0].get_all_points()
        )

        order2Line.set_color(ORANGE)
        
        self.play(
            Create(order2Line).set_run_time(5).set_rate_func(linear)
        )

        order2Group = VGroup(grid2, frame2, order2Label, order2Line)
        self.play(
            order2Group.animate.scale(0.5).to_corner(UL),
            FadeOut(
                copiedOrder1DL,
                copiedOrder1DR,
                copiedOrder1UL,
                copiedOrder1UR
            )
        )
        grid3 = NumberPlane(x_range=[-3, 3, 0.75], y_range=[-3, 3, 0.75], background_line_style={"stroke_color": GREY, "stroke_width": 1}).move_to(ORIGIN)
        frame3 = Rectangle(width=6, height=6, color=YELLOW).move_to(ORIGIN)
        order3Label = Text(" Order 3", font_size=30).to_edge(UP)
        
        self.play(
            Create(frame3),
            Create(grid3),
            Write(order3Label)
        )

        order2CopiedDL = order2Line.copy()
        order2CopiedUL = order2Line.copy()
        order2CopiedUR = order2Line.copy()
        order2CopiedDR = order2Line.copy()
        self.play(
            LaggedStart(
                order2CopiedDL.animate.move_to(grid3.get_center() + DL * 1.5),
                order2CopiedUL.animate.move_to(grid3.get_center() + UL * 1.5),
                order2CopiedUR.animate.move_to(grid3.get_center() + UR * 1.5),
                order2CopiedDR.animate.move_to(grid3.get_center() + DR * 1.5),
                lag_ratio=0.5
            )
        )

        self.play(
            order2CopiedDL.animate.rotate(-PI/2, about_point= order2CopiedDL.get_center()),
            order2CopiedDR.animate.rotate(PI/2, about_point= order2CopiedDR.get_center()),
        )
        self.play(
            order2CopiedDR.animate.apply_matrix([[1,0], [0, -1]], about_point = order2CopiedDR.get_center()),
            order2CopiedDL.animate.apply_matrix([[1,0], [0, -1]], about_point = order2CopiedDL.get_center())
        )

        self.order3Line = VMobject()
        self.order3Line.set_points_as_corners(
                order2CopiedDL.get_all_points()
        )
        self.order3Line.add_points_as_corners(
            order2CopiedUL.get_all_points()
        )
        self.order3Line.add_points_as_corners(
            order2CopiedUR.get_all_points()
        )
        self.order3Line.add_points_as_corners(
            order2CopiedDR.get_all_points()
        )
        
        self.order3Line.set_color(GREEN)
        self.play(
            Create(self.order3Line).set_run_time(4).set_rate_func(linear),
            Wait(4.5)
        )
        self.play(
            VGroup(
                order1LabelGroup,
                hilbertCurveFrame,
                connectedPath1,
                grid,
                grid2,
                frame2,
                order2Line,
                order1Lable,
                order2Label
            ).animate.shift(LEFT * 10)
        )
        self.remove(
            order1LabelGroup,
            hilbertCurveFrame,
            connectedPath1,
            grid,
            grid2,
            frame2,
            order2Line,
            order1Lable,
            order2Label,
            grid3,
            frame3,
            order3Label,
            order2CopiedDL,
            order2CopiedUL,
            order2CopiedUR,
            order2CopiedDR
        )
        
        singleDimension = NumberLine(
            x_range=[0, 1, 0.5],
            unit_size=5,
            numbers_with_elongated_ticks=[-2, 4],
            font_size=24,
        ).shift(LEFT * 4)

        singleDimension.add_labels({0.5: Text("0.5"), 0: Text("0"), 1: Text("1")})
        numberLineDot = Dot(singleDimension.number_to_point(0), color=YELLOW)
        hilbertCurveDot = Dot(self.order3Line.get_corner(DL), color=YELLOW)
        hilbertCurveDot.shift(RIGHT * 3)
        self.play(
            self.order3Line.animate.shift(RIGHT * 3),
            FadeIn(singleDimension, numberLineDot, hilbertCurveDot)
        )
        self.play(
            MoveAlongPath(hilbertCurveDot, self.order3Line).set_rate_func(linear),
            MoveAlongPath(numberLineDot, singleDimension).set_rate_func(linear),
            run_time = 7
        )
        firstDotPairValue = ValueTracker(0.4)
        firstNLPoint = Dot(singleDimension.number_to_point(0.4), color = ORANGE)
        first2DPoint = Dot(self.order3Line.points[int(3004 * 0.4)], color = ORANGE) # 3004
        firstNLPoint.add_updater(lambda dot: dot.move_to(singleDimension.n2p(firstDotPairValue.get_value())))
        first2DPoint.add_updater(lambda dot: dot.move_to(self.order3Line.points[int(3004 * firstDotPairValue.get_value())]))

        secondNLPoint = Dot(singleDimension.number_to_point(0.45), color = BLUE)
        second2DPoint = Dot(self.order3Line.points[int(3004 * 0.45)], color = BLUE)

        self.play(
            FadeIn(firstNLPoint, first2DPoint),
            FadeOut(hilbertCurveDot)
        )

        self.play(
            FadeIn(second2DPoint, secondNLPoint)
        )

        self.play(
            firstDotPairValue.animate.set_value(0.3),
            run_time = 3,
            rate_functions = linear
        )

        self.play(
            Flash(firstNLPoint),
            Flash(secondNLPoint)
        )

        self.play(
            Flash(first2DPoint),
            Flash(second2DPoint)
        )
        propertyLabel = Text("Important Property!\nPoints close to each other on the number line \nare also close along the curve", font_size=20, color = GREEN, t2c={"Important Property!": YELLOW}).move_to(ORIGIN)
        propertyLabel.move_to(singleDimension.get_center() + RIGHT + UP * 2)
        self.play(
            firstDotPairValue.animate.set_value(0.91),
            Write(propertyLabel)
        )

        self.play(
            Flash(firstNLPoint),
            Flash(secondNLPoint)
        )

        self.play(
            Flash(first2DPoint),
            Flash(second2DPoint)
        )

        self.wait(5)

        flatLine = Line(start=second2DPoint.get_center() + LEFT * 0.5, end=second2DPoint.get_center() + RIGHT * 0.5, color=BLUE)
        verticalLine = Line(start=first2DPoint.get_center() + UP * 0.5, end=first2DPoint.get_center() + DOWN * 0.5, color=ORANGE)
        self.play(
            Create(flatLine),
            Create(verticalLine)
        )
        flatLineLabel = Text("f' = 0", font_size=20).next_to(flatLine, UP)
        verticalLineLabel = Text("f' = undefined", font_size=20).next_to(verticalLine, RIGHT)

        self.play(
            Write(flatLineLabel),
            Write(verticalLineLabel)
        )
        self.wait(2)
        possibleSlopeLabel = Text("f'(x) = 0 (horizontal), undefined (vertical)",t2c={"0 (horizontal)": BLUE, "undefined (vertical)": ORANGE}, font_size=20).move_to(propertyLabel.get_center() + DOWN * 3 + LEFT)
        self.play(
            Write(possibleSlopeLabel)
        )

        self.wait(5)

        self.play(
            FadeOut(singleDimension),
            FadeOut(numberLineDot),
            FadeOut(firstNLPoint),
            FadeOut(first2DPoint),
            FadeOut(secondNLPoint),
            FadeOut(second2DPoint),
            FadeOut(flatLine),
            FadeOut(verticalLine),
            FadeOut(flatLineLabel),
            FadeOut(verticalLineLabel),
            FadeOut(propertyLabel),
            FadeOut(possibleSlopeLabel),
            FadeOut(self.order3Line)
        )

    
    def applications(self):
        infilTitle = Text("Applications of the Hilbert Curve\n          3D Printing Infill", font_size=36, weight=BOLD).to_edge(UP)
        infilImage1 = ImageMobject("infill.png").move_to(ORIGIN + RIGHT * 3).scale(0.2)
        infilImage2 = ImageMobject("infill2.png").move_to(ORIGIN + LEFT * 3).scale(0.8)
        self.play(
            FadeIn(infilImage1, infilImage2).set_run_time(2),
            Write(infilTitle)
        )

        self.wait(14)

        self.play(
            FadeOut(infilImage1),
            FadeOut(infilImage2),
            FadeOut(infilTitle)
        )
        beforeImage = ImageMobject("before.png").move_to(ORIGIN + LEFT * 3).scale(1.5)
        afterImage = ImageMobject("after.png").move_to(ORIGIN + RIGHT * 3).scale(1.5)
        compressionTitle = Text("Dithering", font_size=36, weight=BOLD).to_edge(UP)
        self.play(
            FadeIn(beforeImage, afterImage).set_run_time(2),
            Write(compressionTitle)
        )
        self.wait(12)
        self.play(
            FadeOut(beforeImage),
            FadeOut(afterImage),
            FadeOut(compressionTitle)
        )

        tiled_map = self.split_map_image("HilbertMap.png", rows=4, cols=4)
        tiled_map.scale_to_fit_height(4)  # adjust overall visual size
        # self.play(FadeIn(tiled_map, shift=UP), Write(mapTitle))
        # optionally animate tiles individually
        for tile in tiled_map:
            self.play(FadeIn(tile), run_time=0.05)
        mapTitle = Text("Spatial Indexing in Databases", font_size=36, weight=BOLD).to_edge(UP)
        self.play(
            # FadeIn(tiled_map).set_run_time(2),
            Write(mapTitle)
        )
        # self.wait(5)
        grid = NumberPlane(x_range=[-2.5, 2.5, 1.25], y_range=[-2.5, 2.5, 1.25], background_line_style={"stroke_color": WHITE, "stroke_width": 2}).move_to(ORIGIN).scale_to_fit_height(tiled_map.get_height())
        hilbertCurve = VMobject()
        hilbertCurve.set_points_as_corners(self.getHilbertPoints(2, [-2.5, -2.5, 0], 1.25)).move_to(ORIGIN).scale_to_fit_height(grid.get_height() * 3/4)
        hilbertCurve.set_color(YELLOW)
        self.wait(5)
        self.play(
            Create(grid).set_run_time(2)
        )
        self.play(
            Create(hilbertCurve).set_run_time(4).set_rate_func(linear)
        )
        self.play(
            FadeOut(grid),
            FadeOut(hilbertCurve)
        )
        for index, value in enumerate([12, 13,9,8,4, 0,1, 5, 6,2,3,7,11,10,14,15]):
            # rearrange to 1D order
            self.play(
                tiled_map[value].animate.move_to(LEFT*5 + RIGHT * index * tiled_map[value].get_width() * 0.65).scale(0.65),
                run_time=0.3
            )

        self.wait(8)
        self.play(
            FadeOut(tiled_map),
            FadeOut(mapTitle)
        )
        # align all these to the left
        worksCited = Text("Works Cited", font_size=36, weight=BOLD).to_edge(UP)
        cite1 = Text("1. https://towardsdatascience.com/the-beauty-of-space-filling-curves-understanding-the-hilbert-curve/", font_size=20).next_to(worksCited, DOWN * 2).align_to(LEFT)
        cite2 = Text("2. https://everything.explained.today/Hilbert_curve/", font_size=20).next_to(cite1, DOWN).align_to(LEFT)
        cite3 = Text("3. https://ieeexplore.ieee.org/document/9072103", font_size=20).next_to(cite2, DOWN).align_to(LEFT)
        cite4 = Text("4. https://tse4.mm.bing.net/th/id/OIP.SNfyrlY-ZBm_yZ2IMB5USgHaFM?rs=1&pid=ImgDetMain&o=7&rm=3", font_size=20).next_to(cite3, DOWN).align_to(LEFT)
        cite5 = Text("5. https://www.americanscientist.org/article/crinkly-curves", font_size=20).next_to(cite4, DOWN).align_to(LEFT)
        cite6 = Text("6. https://www.compuphase.com/riemer.htm", font_size=20).next_to(cite5, DOWN).align_to(LEFT)
        self.play(
            Write(worksCited).set_run_time(2),
            Write(cite1).set_run_time(2),
            Write(cite2).set_run_time(2),
            Write(cite3).set_run_time(2),
            Write(cite4).set_run_time(2),
            Write(cite5).set_run_time(2),
            Write(cite6).set_run_time(2)
        )
        self.wait(1)




    def construct(self):
        # self.intro() 
        self.tableOfContentsGroup = VGroup()
        # self.tableOfContents()  can shave time here 7s
        # self.hilbertHistory() # 28s
        self.hilbertConstruction()# 1:17 ish
        # self.applications() #37

        
