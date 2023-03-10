import time
from os import path

import pygame

from scripts import CONST
from scripts.main import helper
from scripts.main.data import *

originMult = 1
posMult = 1


class PygameNote:
    def __init__(self, time, position, Approach, refObject):

        self.time = time
        if position == NotePos.Upper:
            color = Color(102, 66, 245)
            Field = Positions.topCentre
            mult = 1
        else:
            mult = -1
            color = Color(245, 64, 64)
            Field = Positions.bottomCentre

        self.Sprite = PygameSprite("file.png",
                                   vector2(0, 200 * mult), SkinSource.user,
                                   Field,
                                   Positions.centre, color, Clocks.audio,
                                   False)
        self.Sprite.scale = 0.2
        self.Sprite.loadFrom(refObject)
        self.Sprite.position = vector2(5550, 5550)

        if position == NotePos.Lower:
            self.Sprite.tag = "LowerElement"
        else:
            self.Sprite.tag = "UpperElement"

        CONST.foregroundSprites.add(self.Sprite)
        self.Sprite.transformations["position"]["beginTime"] = time - Approach
        self.Sprite.transformations["position"]["endTime"] = time + Approach
        self.Sprite.transformations["position"]["beginValue"] = vector2(1000,
                                                                        0)
        self.Sprite.transformations["position"]["endValue"] = vector2(-1000, 0)
        self.Sprite.transformations["position"]["easing"] = EaseTypes.linear
        self.Sprite.transformations["position"]["loop"] = False

    def Miss(self):
        self.Sprite.Color(Color(255, 0, 0))
        self.Sprite.FadeTo(0, 200)
        CONST.Scheduler.AddDelayed(200, CONST.foregroundSprites.remove,
                                   sprite=self.Sprite)

    def Hit(self):
        self.Sprite.ClearTransformations()
        self.Sprite.ScaleTo(0.3, 300, EaseTypes.easeOut)
        self.Sprite.FadeTo(0, 300, EaseTypes.easeOut)
        CONST.Scheduler.AddDelayed(300, CONST.foregroundSprites.remove,
                                   sprite=self.Sprite)


class PygameNotification:
    def __init__(self, text, duration, color=Color(255, 0, 0)):

        self.length = duration

        text = PygameText(text, 15, FontStyle.regular, vector2(0, 0),
                          Positions.bottomRight, Positions.bottomRight)
        textHeight, textWidth = max(text.text.get_height(), 10), max(
            text.text.get_width(), 100)

        background = PygameSprite(CONST.PixelWhite, vector2(0, 0),
                                  SkinSource.local,
                                  Positions.bottomRight, Positions.bottomRight,
                                  Color(0, 0, 0))
        background.Fade(0.8)
        background.VectorScale(vector2(textWidth * 1.5 + 20, textHeight + 10))

        text.position = vector2(0, 2)
        foreGround = PygameSprite(CONST.PixelWhite, vector2(0, 0),
                                  SkinSource.local,
                                  Positions.bottomRight,
                                  Positions.bottomCentre,
                                  color)
        foreGround.VectorScale(vector2(background.image.get_width(), 5))

        foreGround.tag = "SNotification"
        background.tag = "SNotification"
        text.tag = "SNotification"
        self.text = text
        self.bg = background
        self.fg = foreGround

    def show(self):
        for sprite in CONST.overlaySprites.sprites:
            if sprite.tag == "SNotification":
                sprite.posMult = -1
                sprite.posMultY = -1
                sprite.MoveTo(sprite.position.x,
                              sprite.position.y + self.bg.image.get_height() + 2,
                              200, EaseTypes.easeInOut)
        CONST.overlaySprites.add(self.bg)
        CONST.overlaySprites.add(self.fg)
        CONST.overlaySprites.add(self.text)
        self.fg.FadeTo(1, 400, EaseTypes.easeInOut)
        self.fg.VectorScaleTo(vector2(0, 5), self.length)
        self.bg.FadeTo(0.7, 400, EaseTypes.easeInOut)
        self.text.FadeTo(1, 400, EaseTypes.easeInOut)
        self.bg.posMult = -1
        self.bg.posMultY = -1
        self.fg.posMult = -1
        self.fg.posMultY = -1
        CONST.Scheduler.AddDelayed(self.length, self.dispose)

    def dispose(self):

        self.text.FadeTo(0, 400, EaseTypes.easeOut)
        self.fg.FadeTo(0, 400, EaseTypes.easeOut)
        self.bg.FadeTo(0, 400, EaseTypes.easeOut)

        CONST.Scheduler.AddDelayed(400, CONST.overlaySprites.remove,
                                   sprite=self.bg)
        CONST.Scheduler.AddDelayed(400, CONST.overlaySprites.remove,
                                   sprite=self.fg)
        CONST.Scheduler.AddDelayed(400, CONST.overlaySprites.remove,
                                   sprite=self.text)


class NotificationMassive:
    def __init__(self, text, duration, type=NotificationType.Info):

        self.length = duration

        background = PygameSprite(CONST.PixelWhite, vector2(0, 0),
                                  SkinSource.local,
                                  Positions.topLeft, Positions.topLeft,
                                  Color(0, 0, 0))
        background.Fade(0.8)
        background.VectorScale(vector2(1920, 100))
        if type == NotificationType.Info:
            Fgcolor = Color(0, 142, 250)
            textcolor = Color(255, 255, 255)
        elif type == NotificationType.Warning:
            Fgcolor = Color(255, 136, 0)
            textcolor = Color(255, 136, 0)
        else:
            Fgcolor = Color(255, 0, 0)
            textcolor = Color(255, 0, 0)
        foreGround = PygameSprite(CONST.PixelWhite, vector2(0, 100),
                                  SkinSource.local, Positions.topCentre,
                                  Positions.bottomCentre, Fgcolor)
        foreGround.VectorScale(vector2(1900, 10))
        text = PygameText(text, 30, FontStyle.regular, vector2(0, 25),
                          Positions.topCentre, Positions.centre, textcolor)
        foreGround.tag = "Notification"
        background.tag = "Notification"
        text.tag = "Notification"
        self.text = text
        self.bg = background
        self.fg = foreGround

    def show(self):
        for sprite in CONST.overlaySprites.sprites:
            if sprite.tag == "Notification":
                sprite.MoveTo(0, 50, 400, EaseTypes.easeOut)
                sprite.FadeTo(0, 400, EaseTypes.easeOut)
                CONST.Scheduler.AddDelayed(400, CONST.overlaySprites.remove,
                                           sprite=sprite)
        CONST.overlaySprites.add(self.bg)
        CONST.overlaySprites.add(self.fg)
        CONST.overlaySprites.add(self.text)
        self.fg.FadeTo(1, 400, EaseTypes.easeInOut)
        self.fg.VectorScaleTo(vector2(0, 10), self.length)
        self.bg.FadeTo(0.7, 400, EaseTypes.easeInOut)
        self.text.FadeTo(1, 400, EaseTypes.easeInOut)

        CONST.Scheduler.AddDelayed(self.length, self.dispose)

    def dispose(self):

        self.text.FadeTo(0, 400, EaseTypes.easeOut)
        self.fg.FadeTo(0, 400, EaseTypes.easeOut)
        self.bg.FadeTo(0, 400, EaseTypes.easeOut)

        CONST.Scheduler.AddDelayed(400, CONST.overlaySprites.remove,
                                   sprite=self.bg)
        CONST.Scheduler.AddDelayed(400, CONST.overlaySprites.remove,
                                   sprite=self.fg)
        CONST.Scheduler.AddDelayed(400, CONST.overlaySprites.remove,
                                   sprite=self.text)


class PygameButton:
    def __init__(self, text, size, style=FontStyle.regular,
                 position=vector2(0, 0), color=Color(255, 255, 255, 255)):

        self.originPosition = position
        self.position = vector2(0, 0)
        self.color = color
        self.size = size

        self.centreButton = PygameSprite(CONST.PixelWhite, position=position,
                                         skinSource=SkinSource.local,
                                         field=Positions.topLeft,
                                         origin=Positions.centre, color=color)

        self.centreButton.VectorScale(size)
        offset = 0.57
        pos = position
        poss = Positions

        self.text = PygameText(text, (0.8 * size.y), style,
                               position=vector2(pos.x * offset,
                                                pos.y * offset - 15),
                               field=poss.topLeft, origin=poss.centre)

        self.rightButton = PygameSprite("button-right.png",
                                        vector2(pos.x + (size.x / 2) - 1,
                                                pos.y), SkinSource.local,
                                        poss.topLeft, poss.centreLeft, color)

        self.leftButton = PygameSprite("button-left.png",
                                       vector2(pos.x - (size.x / 2) + 1,
                                               pos.y), SkinSource.local,
                                       poss.topLeft, poss.centreRight, color)

        self.rightButton.Scale((1 / 500) * size.y)
        self.leftButton.Scale((1 / 500) * size.y)

        self.tag = ""
        self.onhover = []
        self.onhoverlost = []
        self.onclick = []
        self.isonHover = False
        self.enabled = True

    def onHover(self, function, **kwargs):
        self.onhover.append([function, kwargs])

    def onHoverLost(self, function, **kwargs):
        self.onhoverlost.append([function, kwargs])

    def onClick(self, function, **kwargs):
        self.onclick.append([function, kwargs])

    def enable(self):
        self.enabled = True
        self.centreButton.enable()
        self.rightButton.enable()
        self.leftButton.enable()
        self.text.enable()

    def disable(self):
        self.enabled = False
        self.centreButton.disable()
        self.rightButton.disable()
        self.leftButton.disable()
        self.text.disable()

    def __onHover__(self):
        for hoverAction in self.onhover:
            if hoverAction[1] == {}:
                hoverAction[0]()
            else:
                hoverAction[0](**hoverAction[1])
        self.centreButton.VectorScaleTo(vector2(self.size.x + 10, self.size.y),
                                        200)
        self.centreButton.Color(
            Color(min(self.color.r + 30, 255), min(self.color.g + 30, 255),
                  min(self.color.b + 30, 255)))
        self.rightButton.Color(
            Color(min(self.color.r + 30, 255), min(self.color.g + 30, 255),
                  min(self.color.b + 30, 255)))
        self.leftButton.Color(
            Color(min(self.color.r + 30, 255), min(self.color.g + 30, 255),
                  min(self.color.b + 30, 255)))

    def ClearTransformations(self):
        pass

    def __onHoverLost__(self):
        for hoverLostAction in self.onhoverlost:
            if hoverLostAction[1] == {}:
                hoverLostAction[0]()
            else:
                hoverLostAction[0](hoverLostAction[1])
        self.centreButton.VectorScaleTo(vector2(self.size.x + 10, self.size.y),
                                        200)
        self.centreButton.Color(self.color)
        self.rightButton.Color(self.color)
        self.leftButton.Color(self.color)

    def __onClick__(self):
        for click in self.onclick:
            if click[1] == {}:
                click[0]()
            else:
                click[0](**click[1])
        self.centreButton.Color(Color(255, 255, 255))
        self.centreButton.FadeColorTo(self.color, 300, EaseTypes.easeInOut)
        self.rightButton.Color(Color(255, 255, 255))
        self.rightButton.FadeColorTo(self.color, 300, EaseTypes.easeInOut)
        self.leftButton.Color(Color(255, 255, 255))
        self.leftButton.FadeColorTo(self.color, 300, EaseTypes.easeInOut)

    def Position(self, position):
        self.position = position
        self.centreButton.position = position
        self.rightButton.position = position
        self.leftButton.position = position
        self.text.position = position

    def Fade(self, x):
        self.centreButton.Fade(x)
        self.text.Fade(x)
        self.leftButton.Fade(x)
        self.rightButton.Fade(x)

    def FadeTo(self, value, duration, easing=EaseTypes.linear):
        self.centreButton.FadeTo(value, duration, easing)
        self.text.FadeTo(value, duration, easing)
        self.leftButton.FadeTo(value, duration, easing)
        self.rightButton.FadeTo(value, duration, easing)

    def draw(self):
        self.centreButton.draw()
        self.rightButton.draw()
        self.leftButton.draw()
        self.text.draw()
        if self.enabled:
            if ((self.centreButton.isonHover or self.rightButton.isonHover or
                 self.leftButton.isonHover) and not self.isonHover):
                self.__onHover__()
                self.isonHover = True
            elif not ((self.centreButton.isonHover or
                       self.rightButton.isonHover or
                       self.leftButton.isonHover) and self.isonHover):
                self.__onHoverLost__()
                self.isonHover = False


class PygameText:

    def __init__(self, text, textSize, style=FontStyle.regular,
                 position=vector2(0, 0), field=Positions.topLeft,
                 origin=Positions.topLeft, color=Color(255, 255, 255, 255),
                 clock=Clocks.game):
        global originMult
        originMult = 1 / (CONST.windowManager.getPixelSize())

        mult = int(textSize * 2.66)

        self.font = pygame.font.Font(
            CONST.currentDirectory + "/data/fonts/Torus-" + style, mult)
        self.text = self.font.render(text, True,
                                     (color.r, color.g, color.b, color.a))
        self.text = self.text.convert_alpha()
        self.field = field
        self.origin = origin
        self.Clock = clock
        self.originPosition = position
        self.posMult = posMult
        self.posMultY = posMult
        self.position = vector2(0, 0)
        self.scale = 1
        self.tag = ""
        self.transformations = {"scale": {}, "fade": {}, "VectorScale": {},
                                "position": {}, "colorFade": {},
                                "rotation": {}}
        self.alpha = 1
        self.vectorScale = vector2(1, 1)
        self.originColor = color
        self.color = color
        self.rotation = 0
        self.textSize = textSize * CONST.windowManager.getPixelSize() * 3 * 1.3
        self.offset = vector2(0, 0)
        self.effectivePosition = vector2(0, 0)
        self.onhover = []
        self.onhoverlost = []
        self.onClick = []
        self.isonHover = False
        self.enabled = True

        width = self.text.get_width()
        height = self.text.get_height()
        self.srcText = self.text.convert_alpha()
        self.unBlendedImg = self.text.convert_alpha()
        colorR = self.color.r
        colorG = self.color.g
        colorB = self.color.b
        colorA = self.color.a
        self.srcText.fill((colorR, colorG, colorB, colorA),
                          special_flags=pygame.BLEND_RGBA_MULT)

        self.text = pygame.transform.scale(self.srcText, (
            int(width * CONST.windowManager.getPixelSize() * (self.scale) / 3),
            int(height * CONST.windowManager.getPixelSize() * (
                self.scale) / 3)))
        self.UpdateStats()

    def __onHover__(self):
        for hoverAction in self.onhover:
            if hoverAction[1] == {}:
                hoverAction[0]()
            else:
                hoverAction[0](hoverAction[1])

    def __onHoverLost__(self):
        for hoverLostAction in self.onhoverlost:
            if hoverLostAction[1] == {}:
                hoverLostAction[0]()
            else:
                hoverLostAction[0](hoverLostAction[1])

    def __onClick__(self):
        for click in self.onClick:
            click[0](click[1])

    def disable(self):
        """
        Disable any transition and every input if enabled
        """
        self.enabled = False
        self.text.set_alpha(int((self.alpha / 4) * 255))
        self.HiddenColor(
            Color(self.color.r * 0.3, self.color.g * 0.3, self.color.b * 0.3))

    def enable(self):
        """
        Enable any transition and every input if disabled
        """
        self.enabled = True
        self.text.set_alpha(self.alpha)
        self.HiddenColor(self.color)

    def HiddenColor(self, color):
        """
        Same as Color, but will not register color in variable, so can be cancelled with obj.Color(obj.color)
        :param color: Color of the sprite
        """
        self.srcText = self.unBlendedImg.convert_alpha()
        self.srcText.fill((color.r, color.g, color.b, color.a),
                          special_flags=pygame.BLEND_RGBA_MULT)
        self.Scale(self.scale)

    def onHover(self, function, **kwargs):
        self.onhover.append([function, kwargs])

    def onHoverLost(self, function, **kwargs):
        self.onhoverlost.append([function, kwargs])

    def onClick(self, function, **kwargs):
        self.onClick.append([function, kwargs])

    def Rotate(self, deg, fromScale=False):
        self.rotation = deg
        self.text = pygame.transform.rotate(self.text, deg)
        self.UpdateStats()

    def Text(self, text):
        self.unBlendedImg = self.font.render(text, True, (
            self.color.r, self.color.g, self.color.b, self.color.a))
        self.srcText = self.font.render(text, True, (
            self.color.r, self.color.g, self.color.b, self.color.a))
        self.text = self.font.render(text, True, (
            self.color.r, self.color.g, self.color.b, self.color.a))
        self.UpdateStats()
        self.Scale(self.scale)
        self.Fade(self.alpha)

    def Scale(self, x):
        if CONST.windowManager.getPixelSize() > 1:
            sx = (1 / CONST.windowManager.getPixelSize()) / 2.2
        else:
            sx = (CONST.windowManager.getPixelSize()) / 2.2
        self.scale = x
        width = self.srcText.get_width()
        height = self.srcText.get_height()
        self.text = pygame.transform.scale(self.srcText, (
            int(width * CONST.windowManager.getPixelSize() * sx * x * self.vectorScale.x),
            int(height * CONST.windowManager.getPixelSize() * sx * x * self.vectorScale.y)))
        self.UpdateStats()

    def Color(self, color):
        self.srcText = self.unBlendedImg.convert_alpha()
        self.color = color
        self.srcText.fill((color.r, color.g, color.b, color.a),
                          special_flags=pygame.BLEND_RGBA_MULT)
        self.Scale(self.scale)

    def VectorScale(self, vectorScale):
        self.vectorScale = vectorScale
        self.Scale(self.scale)

    def Fade(self, x):
        self.alpha = x
        self.text.set_alpha(255 * x)

    def MoveTo(self, x, y, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["position"]["beginTime"] = time.time() * 1000
        self.transformations["position"][
            "endTime"] = time.time() * 1000 + duration
        self.transformations["position"]["beginValue"] = self.position
        self.transformations["position"]["endValue"] = vector2(x, y)
        self.transformations["position"]["easing"] = easing
        self.transformations["position"]["loop"] = loop

    def FadeTo(self, value, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["fade"]["beginTime"] = time.time() * 1000
        self.transformations["fade"]["endTime"] = time.time() * 1000 + duration
        self.transformations["fade"]["beginValue"] = self.alpha
        self.transformations["fade"]["endValue"] = value
        self.transformations["fade"]["easing"] = easing
        self.transformations["fade"]["loop"] = loop

    def FadeColorTo(self, color, duration, easing=EaseTypes.linear,
                    loop=False):
        self.transformations["colorFade"]["beginTime"] = time.time() * 1000
        self.transformations["colorFade"][
            "endTime"] = time.time() * 1000 + duration
        self.transformations["colorFade"]["beginValue"] = self.color
        self.transformations["colorFade"]["endValue"] = color
        self.transformations["colorFade"]["easing"] = easing
        self.transformations["colorFade"]["loop"] = loop

    def VectorScaleTo(self, scale, duration, easing=EaseTypes.linear,
                      loop=False):
        self.transformations["VectorScale"]["beginTime"] = time.time() * 1000
        self.transformations["VectorScale"][
            "endTime"] = time.time() * 1000 + duration
        self.transformations["VectorScale"]["beginValue"] = self.vectorScale
        self.transformations["VectorScale"]["endValue"] = scale
        self.transformations["VectorScale"]["easing"] = easing
        self.transformations["VectorScale"]["loop"] = loop

    def ScaleTo(self, scale, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["scale"]["beginTime"] = time.time() * 1000
        self.transformations["scale"][
            "endTime"] = time.time() * 1000 + duration
        self.transformations["scale"]["beginValue"] = self.scale
        self.transformations["scale"]["endValue"] = scale
        self.transformations["scale"]["easing"] = easing
        self.transformations["scale"]["loop"] = loop

    def ClearTransformations(self, type=None):
        self.transformations = {"scale": {}, "fade": {}, "VectorScale": {},
                                "position": {}, "colorFade": {},
                                "rotation": {}}

    def UpdateStats(self):
        if self.field == Positions.topLeft:
            self.offset = vector2(0, 0)
        elif self.field == Positions.topCentre:
            self.offset = vector2(CONST.windowManager.width / 2, 0)
        elif self.field == Positions.topRight:
            self.offset = vector2(CONST.windowManager.width, 0)
            self.posMult = -posMult
        elif self.field == Positions.centreLeft:
            self.offset = vector2(0, CONST.windowManager.height / 2)
        elif self.field == Positions.centre:
            self.offset = vector2(CONST.windowManager.width / 2,
                                  CONST.windowManager.height / 2)
        elif self.field == Positions.centreRight:
            self.offset = vector2(CONST.windowManager.width,
                                  CONST.windowManager.height / 2)
            self.posMult = -posMult
        elif self.field == Positions.bottomLeft:
            self.offset = vector2(0, CONST.windowManager.height)
            self.posMultY = -posMult
        elif self.field == Positions.bottomCentre:
            self.offset = vector2(CONST.windowManager.width / 2,
                                  CONST.windowManager.height)
            self.posMultY = -posMult
        elif self.field == Positions.bottomRight:
            self.offset = vector2(CONST.windowManager.width,
                                  CONST.windowManager.height)
            self.posMultY = -posMult
            self.posMult = -posMult
        width = self.text.get_width()
        height = self.text.get_height()
        if self.origin == Positions.topCentre:
            self.offset.x -= width / 2
        elif self.origin == Positions.topRight:
            self.offset.x -= width
        elif self.origin == Positions.centreLeft:
            self.offset.y -= height / 2
        elif self.origin == Positions.centre:
            self.offset.x -= width / 2
            self.offset.y -= height / 2
        elif self.origin == Positions.centreRight:
            self.offset.x -= width
            self.offset.y -= height / 2
        elif self.origin == Positions.bottomLeft:
            self.offset.y -= height
        elif self.origin == Positions.bottomCentre:
            self.offset.x -= width / 2
            self.offset.y -= height
        elif self.origin == Positions.bottomRight:
            self.offset.x -= width
            self.offset.y -= height
        self.effectivePosition = vector2(self.originPosition.x + self.offset.x,
                                         self.originPosition.y + self.offset.y)

    def draw(self):
        if self.enabled:
            if self.text.get_rect().collidepoint(
                    pygame.mouse.get_pos()) and not self.isonHover:
                self.isonHover = True
                self.__onHover__()
            elif not self.text.get_rect().collidepoint(
                    pygame.mouse.get_pos()) and self.isonHover:
                self.isonHover = False
                self.__onHoverLost__()
            if self.Clock == Clocks.game:
                now = time.time() * 1000
            else:
                now = pygame.mixer.music.get_pos()

            if self.transformations["rotation"] != {}:
                beginTime = self.transformations["rotation"]["beginTime"]
                endtime = self.transformations["rotation"]["endTime"]
                beginValue = self.transformations["rotation"]["beginValue"]
                endValue = self.transformations["rotation"]["endValue"]
                easing = self.transformations["rotation"]["easing"]
                if self.scale == endValue:
                    if self.transformations["rotation"]["loop"]:
                        duration = self.transformations["rotation"][
                                       "endTime"] - \
                                   self.transformations["rotation"][
                                       "beginTime"]
                        self.transformations["rotation"]["beginTime"] = now
                        self.transformations["rotation"][
                            "endTime"] = now + duration
                        self.transformations["rotation"][
                            "beginValue"] = endValue
                        self.transformations["rotation"][
                            "endValue"] = beginValue
                    else:
                        self.transformations["rotation"] = {}
                elif now > beginTime:
                    self.Scale(self.scale)
                    if self.Clock == Clocks.game:
                        self.Rotate(
                            helper.getTimeValue(beginTime, endtime, beginValue,
                                                endValue, easing))
                    else:
                        self.Rotate(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValue, endValue,
                                                     easing))

            if self.transformations["scale"] != {}:
                beginTime = self.transformations["scale"]["beginTime"]
                endtime = self.transformations["scale"]["endTime"]
                beginValue = self.transformations["scale"]["beginValue"]
                endValue = self.transformations["scale"]["endValue"]
                easing = self.transformations["scale"]["easing"]
                if self.scale == endValue:
                    if self.transformations["scale"]["loop"]:
                        duration = self.transformations["scale"]["endTime"] - \
                                   self.transformations["scale"][
                                       "beginTime"]
                        self.transformations["scale"]["beginTime"] = now
                        self.transformations["scale"][
                            "endTime"] = now + duration
                        self.transformations["scale"]["beginValue"] = endValue
                        self.transformations["scale"]["endValue"] = beginValue
                    else:
                        self.transformations["scale"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Scale(
                            helper.getTimeValue(beginTime, endtime, beginValue,
                                                endValue, easing))
                    else:
                        self.Scale(helper.getAudioTimeValue(beginTime, endtime,
                                                            beginValue,
                                                            endValue, easing))

            if self.transformations["fade"] != {}:
                beginTime = self.transformations["fade"]["beginTime"]
                endtime = self.transformations["fade"]["endTime"]
                beginValue = self.transformations["fade"]["beginValue"]
                endValue = self.transformations["fade"]["endValue"]
                easing = self.transformations["fade"]["easing"]
                if self.alpha == endValue:
                    if self.transformations["fade"]["loop"]:
                        duration = self.transformations["fade"]["endTime"] - \
                                   self.transformations["fade"][
                                       "beginTime"]
                        self.transformations["fade"]["beginTime"] = now
                        self.transformations["fade"][
                            "endTime"] = now + duration
                        self.transformations["fade"]["beginValue"] = endValue
                        self.transformations["fade"]["endValue"] = beginValue
                    else:
                        self.transformations["fade"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Fade(
                            helper.getTimeValue(beginTime, endtime, beginValue,
                                                endValue, easing))
                    else:
                        self.Fade(helper.getAudioTimeValue(beginTime, endtime,
                                                           beginValue,
                                                           endValue, easing))
            if self.transformations["VectorScale"] != {}:
                beginTime = self.transformations["VectorScale"]["beginTime"]
                endtime = self.transformations["VectorScale"]["endTime"]
                beginValueX = self.transformations["VectorScale"][
                    "beginValue"].x
                endValueX = self.transformations["VectorScale"]["endValue"].x
                beginValueY = self.transformations["VectorScale"][
                    "beginValue"].y
                endValueY = self.transformations["VectorScale"]["endValue"].y
                easing = self.transformations["VectorScale"]["easing"]
                if self.vectorScale.x == endValueX and self.vectorScale.y == endValueY:
                    if self.transformations["VectorScale"]["loop"]:
                        duration = self.transformations["VectorScale"][
                                       "endTime"] - \
                                   self.transformations["VectorScale"][
                                       "beginTime"]
                        self.transformations["VectorScale"]["beginTime"] = now
                        self.transformations["VectorScale"][
                            "endTime"] = now + duration
                        self.transformations["VectorScale"][
                            "beginValue"] = vector2(endValueX, endValueY)
                        self.transformations["VectorScale"][
                            "endValue"] = vector2(beginValueX, beginValueY)
                    else:
                        self.transformations["VectorScale"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.VectorScale(
                            vector2(helper.getTimeValue(beginTime, endtime,
                                                        beginValueX, endValueX,
                                                        easing),
                                    helper.getTimeValue(beginTime, endtime,
                                                        beginValueY, endValueY,
                                                        easing)))
                    else:
                        self.VectorScale(
                            vector2(
                                helper.getAudioTimeValue(beginTime, endtime,
                                                         beginValueX,
                                                         endValueX, easing),
                                helper.getAudioTimeValue(beginTime, endtime,
                                                         beginValueY,
                                                         endValueY, easing)))

            if self.transformations["colorFade"] != {}:
                beginTime = self.transformations["colorFade"]["beginTime"]
                endtime = self.transformations["colorFade"]["endTime"]

                beginValueR = self.transformations["colorFade"]["beginValue"].r
                endValueR = self.transformations["colorFade"]["endValue"].r

                beginValueG = self.transformations["colorFade"]["beginValue"].g
                endValueG = self.transformations["colorFade"]["endValue"].g

                beginValueB = self.transformations["colorFade"]["beginValue"].b
                endValueB = self.transformations["colorFade"]["endValue"].b

                easing = self.transformations["colorFade"]["easing"]
                if self.color.r == endValueR and self.color.g == endValueG and self.color.b == endValueB:
                    if self.transformations["colorFade"]["loop"]:
                        duration = self.transformations["colorFade"][
                                       "endTime"] - \
                                   self.transformations["colorFade"][
                                       "beginTime"]
                        self.transformations["colorFade"]["beginTime"] = now
                        self.transformations["colorFade"][
                            "endTime"] = now + duration
                        self.transformations["colorFade"][
                            "beginValue"] = Color(endValueR, endValueG,
                                                  endValueB)
                        self.transformations["colorFade"]["endValue"] = Color(
                            beginValueR, beginValueG, beginValueB)
                    else:
                        self.transformations["colorFade"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Color(Color(
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueR, endValueR,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueG, endValueG,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueB, endValueB,
                                                easing)))
                    else:
                        self.Color(Color(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueR, endValueR,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueG, endValueG,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueB, endValueB,
                                                     easing)))

            if self.transformations["position"] != {}:
                beginTime = self.transformations["position"]["beginTime"]
                endtime = self.transformations["position"]["endTime"]
                beginValueX = self.transformations["position"]["beginValue"].x
                endValueX = self.transformations["position"]["endValue"].x
                beginValueY = self.transformations["position"]["beginValue"].y
                endValueY = self.transformations["position"]["endValue"].y
                easing = self.transformations["position"]["easing"]
                if self.position.x == endValueX and self.position.y == endValueY:
                    if self.transformations["position"]["loop"]:
                        duration = self.transformations["position"][
                                       "endTime"] - \
                                   self.transformations["position"][
                                       "beginTime"]
                        self.transformations["position"]["beginTime"] = now
                        self.transformations["position"][
                            "endTime"] = now + duration
                        self.transformations["position"][
                            "beginValue"] = vector2(endValueX, endValueY)
                        self.transformations["position"]["endValue"] = vector2(
                            beginValueX, beginValueY)
                    else:
                        self.transformations["position"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.position = vector2(
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueX, endValueX,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueY, endValueY,
                                                easing))
                    else:
                        self.position = vector2(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueX, endValueX,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueY, endValueY,
                                                     easing))
        self.UpdateStats()
        if self.alpha != 0:
            CONST.surface.blit(self.text,
                               (
                                   self.effectivePosition.x + CONST.windowManager.getPixelSize() *
                                   int(((
                                                self.originPosition.x + self.position.x * originMult) * self.posMult) * (
                                               CONST.windowManager.getPixelSize() / 1.3)),
                                   self.effectivePosition.y + CONST.windowManager.getPixelSize() *
                                   int(((
                                                self.originPosition.y + self.position.y * originMult) * self.posMultY)) * (
                                           CONST.windowManager.getPixelSize() / 1.3)))


class PygameSprite:
    """The main sprite class to make things more easier"""

    def __init__(self, filename, position, skinSource, field, origin,
                 color=Color(255, 255, 255, 255), clock=Clocks.game,
                 load=True):
        """
        :param filename: the filename of the file (relative to skinSource)
        :param position: the Origin position of the sprite (relative to the field and origin)
        :param skinSource: SkinSource is the directory of the sprite,
            user = Take from the user skin, if not present, take from local SkinSource
            local = Take from the dir /data/sprites/<filename>
        :param field: Anchor of the sprite, where should it be placed on the screen
        :param origin: the origin of the sprite, if the (0,0) is on the top or the bottom of the sprite, or even center !
        :param color: Color of the sprite, act as a Multiplier mask on the sprite (useful for glob.PixelWhite to get a color)
        :param clock: How the transformations should be applied
        :param load: is the sprite should be directly loaded, mainly used in game to use the same object instead of overloading
            the ram with copy of same object
        """
        if load:
            if skinSource == SkinSource.user and path.exists(
                    CONST.currentDirectory + "/.user/skins/" + CONST.currentSkin + "/" + filename):
                self.image = pygame.image.load(
                    CONST.currentDirectory + "/.user/skins/" + CONST.currentSkin + "/" + filename)
            elif skinSource == SkinSource.absolute:
                self.image = pygame.image.load(filename)
            else:
                self.image = pygame.image.load(
                    CONST.currentDirectory + "/data/sprites/" + filename)
            self.image = self.image.convert_alpha()
        else:
            self.image = None
        self.filename = filename
        self.field = field
        self.Clock = clock
        self.origin = origin
        self.originPosition = position
        self.posMult = 1
        self.posMultY = 1
        self.position = vector2(0, 0)
        self.scale = 1
        self.tag = ""
        self.transformations = {"scale": {}, "fade": {}, "VectorScale": {},
                                "position": {}, "colorFade": {},
                                "rotation": {}}
        self.alpha = 1
        self.vectorScale = vector2(1, 1)
        self.originColor = color
        self.color = color
        self.rotation = 0
        self.offset = None

        self.isonHover = False
        self.onhover = []
        self.onhoverlost = []
        self.onclick = []
        self.enabled = True
        self.data = []

        if load:
            width = self.image.get_width()
            height = self.image.get_height()
            self.srcImg = self.image.convert_alpha()
            self.unBlendedImg = self.image.convert_alpha()
            colorR = self.color.r
            colorG = self.color.g
            colorB = self.color.b
            colorA = self.color.a
            self.srcImg.fill((colorR, colorG, colorB, colorA),
                             special_flags=pygame.BLEND_RGBA_MULT)
            self.image = pygame.transform.scale(self.srcImg, (
                int(width * CONST.windowManager.getPixelSize() * self.scale),
                int(height * CONST.windowManager.getPixelSize() * self.scale)))
            self.UpdateStats()
        else:
            self.srcImg = None
            self.unBlendedImg = None

    def loadFrom(self, other):
        """Used to use this sprite from another sprite as reference, and avoiding ram overloading, but remind that any transformaiton except position change will result to a copy of the sprite"""
        self.srcImg = other.srcImg
        self.unBlendedImg = other.unBlendedImg
        self.image = other.image
        self.UpdateStats()

    def Horiflip(self):
        self.srcImg = pygame.transform.flip(self.srcImg, False, True)
        self.Scale(self.scale)

    def Vertflip(self):
        self.srcImg = pygame.transform.flip(self.srcImg, True, False)
        self.Scale(self.scale)

    def changeImageFromString(self, string, size):
        self.unBlendedImg = pygame.image.fromstring(string, size,
                                                    "RGBA").convert_alpha()
        self.Color(self.color)

    def __onHover__(self):
        for hoverAction in self.onhover:
            if hoverAction[1] == {}:
                hoverAction[0]()
            else:
                hoverAction[0](**hoverAction[1])

    def __onHoverLost__(self):
        for hoverLostAction in self.onhoverlost:
            if hoverLostAction[1] == {}:
                hoverLostAction[0]()
            else:
                hoverLostAction[0](**hoverLostAction[1])

    def __onClick__(self):
        for onClick in self.onclick:
            if onClick[1] == {}:
                onClick[0]()
            else:
                onClick[0](**onClick[1])

    def onHover(self, function, **kwargs):
        """
        (can be called multiple times)
        Add a task to do when sprite is enabled and just got hovered
        :param function: Actual function (DO NOT CALL IT, just put self.thing, NOT self.thing())
        :param kwargs: Add as many as arguments for the function you pointed before
        """
        self.onhover.append([function, kwargs])

    def disable(self):
        """
        Disable any transition and every input if enabled
        """
        self.enabled = False
        self.image.set_alpha(int((self.alpha / 4) * 255))
        self.HiddenColor(
            Color(self.color.r * 0.3, self.color.g * 0.3, self.color.b * 0.3))

    def enable(self):
        """
        Enable any transition and every input if disabled
        """
        self.enabled = True
        self.image.set_alpha(self.alpha)
        self.HiddenColor(self.color)

    def onHoverLost(self, function, **kwargs):
        """
        (can be called multiple times)
        Add a task to do when sprite is enabled and just lost hover
        :param function: Actual function (DO NOT CALL IT, just put self.thing, NOT self.thing())
        :param kwargs: Add as many as arguments for the function you pointed before
        """
        self.onhoverlost.append([function, kwargs])

    def onClick(self, function, **kwargs):
        """
        (can be called multiple times)
        Add a task to do when sprite is clicked on
        :param function: Actual function (DO NOT CALL IT, just put self.thing, NOT self.thing())
        :param kwargs: Add as many as arguments for the function you pointed before
        """
        self.onclick.append([function, kwargs])

    def Rotate(self, deg):
        """
        Rotate the sprite (must be done after scaling or color change)
        :param deg: rotation deg from 1 to 360
        """
        self.rotation = deg
        self.image = pygame.transform.rotate(self.image, deg)
        self.UpdateStats(True)

    def borderBounds(self, borderRadius):
        """
        :param borderRadius: BorderRadius of the sprite, refer to css border-radius
        """
        self.image = pygame.image.fromstring(
            helper.cornerBounds(self, borderRadius), self.image.get_size(),
            "RGBA").convert_alpha()

    def crop(self, x, y):
        """
        Image cropping (must be done after scaling) (will take the center of the image as origin)
        :param x: Width of the image
        :param y: Height of the image
        """
        offset = vector2(0, 0)
        width = self.unBlendedImg.get_width()
        height = self.unBlendedImg.get_height()
        self.Scale(1920 / width)
        self.image = self.image.subsurface((width / 2, height / 2 - (y / 2),
                                            x * CONST.windowManager.getPixelSize(),
                                            y * CONST.windowManager.getPixelSize()))
        self.UpdateStats()

    def Scale(self, x):
        """
        Image rescaling
        :param x: Scale factor
        """
        self.scale = x
        width = self.srcImg.get_width()
        height = self.srcImg.get_height()
        self.image = pygame.transform.scale(self.srcImg, (
            int(width * CONST.windowManager.getPixelSize() * x * self.vectorScale.x),
            int(height * CONST.windowManager.getPixelSize() * x * self.vectorScale.y)))
        self.image.set_alpha(255 * self.alpha)
        self.UpdateStats()

    def Color(self, color):
        """
        Multiply mask Color (will replace other Color transformations)
        :param color: Color of the sprite
        """
        self.srcImg = self.unBlendedImg.convert_alpha()
        self.color = color
        self.srcImg.fill((color.r, color.g, color.b, color.a),
                         special_flags=pygame.BLEND_RGBA_MULT)
        self.Scale(self.scale)

    def HiddenColor(self, color):
        """
        Same as Color, but will not register color in variable, so can be cancelled with obj.Color(obj.color)
        :param color: Color of the sprite
        """
        self.srcImg = self.unBlendedImg.convert_alpha()
        self.srcImg.fill((color.r, color.g, color.b, color.a),
                         special_flags=pygame.BLEND_RGBA_MULT)
        self.Scale(self.scale)

    def FillColor(self, Color):
        """
        Will add a normal filter on the sprite, act like Color
        :param color: Color of the sprite
        """
        self.Color(self.color)
        s = pygame.Surface((self.srcImg.get_width(), self.srcImg.get_height()))
        s.set_alpha(Color.a)
        s.fill((Color.r, Color.g, Color.b))
        self.srcImg.blit(s, (0, 0))
        self.Scale(self.scale)

    def AlphaMask(self, mask):
        """
        Allow Multiply Masking, mainly used for alpha masking but can be use for everything, must be put after Scaling
        :param mask: mask to apply to the sprite (relative to /data/sprites/masks/<mask>)
        """
        mask = CONST.currentDirectory + "/data/sprites/masks/" + mask
        mask = pygame.image.load(mask)
        mask = pygame.transform.scale(mask, (
            int(self.image.get_width()), int(self.image.get_height())))
        self.image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def TopGradiant(self, color, style):
        """
        Apply gradiant to the image from top to bottom
        :param color: Color of the gradiant
        :param style: /data/sprites/gradiants/gradiant-<style>.png
        """
        try:
            gradiant = pygame.image.load(
                CONST.currentDirectory + "/data/sprites/gradiants/gradiant-" + style + ".png").convert_alpha()
        except:
            gradiant = pygame.image.load(
                CONST.currentDirectory + "/data/sprites/gradiants/gradiant-full.png").convert_alpha()

        gradiant = pygame.transform.scale(gradiant, (
            self.srcImg.get_height(), self.srcImg.get_width()))
        gradiant.fill(((color.r, color.g, color.b, color.a)),
                      special_flags=pygame.BLEND_RGBA_MULT)
        gradiant = pygame.transform.rotate(gradiant, -90)
        self.Color(self.color)
        self.srcImg.blit(gradiant, (0, 0))
        self.Scale(self.scale)

    def BottomGradiant(self, color, style):
        """
        Apply gradiant to the image from bottom to top
        :param color: Color of the gradiant
        :param style: /data/sprites/gradiants/gradiant-<style>.png
        """
        try:
            gradiant = pygame.image.load(
                CONST.currentDirectory + "/data/sprites/gradiants/gradiant-" + style + ".png").convert_alpha()
        except:
            gradiant = pygame.image.load(
                CONST.currentDirectory + "/data/sprites/gradiants/gradiant-full.png").convert_alpha()

        gradiant = pygame.transform.scale(gradiant, (
            self.srcImg.get_height(), self.srcImg.get_width()))
        gradiant.fill(((color.r, color.g, color.b, color.a)),
                      special_flags=pygame.BLEND_RGBA_MULT)
        gradiant = pygame.transform.rotate(gradiant, 90)
        self.Color(self.color)
        self.srcImg.blit(gradiant, (0, 0))
        self.Scale(self.scale)

    def VectorScale(self, vectorScale):
        """
        Allow Different Width/height Scaling, Useful for glob.WhitePixel to fill surfaces
        :param vectorScale:
        :return:
        """
        self.vectorScale = vectorScale
        self.Scale(self.scale)

    def Fade(self, x):
        """
        Set global opacity of the sprite
        :param x: 0 to 1 float opacity
        """
        self.alpha = x
        self.image.set_alpha(255 * x)

    def MoveTo(self, x, y, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["position"][
            "beginTime"] = time.time() * 1000 if self.Clock == Clocks.game else pygame.mixer.music.get_pos()
        self.transformations["position"][
            "endTime"] = time.time() * 1000 + duration if self.Clock == Clocks.game else pygame.mixer.music.get_pos() + duration
        self.transformations["position"]["beginValue"] = self.position
        self.transformations["position"]["endValue"] = vector2(x, y)
        self.transformations["position"]["easing"] = easing
        self.transformations["position"]["loop"] = loop

    def FadeTo(self, value, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["fade"][
            "beginTime"] = time.time() * 1000 if self.Clock == Clocks.game else pygame.mixer.music.get_pos()
        self.transformations["fade"][
            "endTime"] = time.time() * 1000 + duration if self.Clock == Clocks.game else pygame.mixer.music.get_pos() + duration
        self.transformations["fade"]["beginValue"] = self.alpha
        self.transformations["fade"]["endValue"] = value
        self.transformations["fade"]["easing"] = easing
        self.transformations["fade"]["loop"] = loop

    def FadeColorTo(self, color, duration, easing=EaseTypes.linear,
                    loop=False):
        self.transformations["colorFade"][
            "beginTime"] = time.time() * 1000 if self.Clock == Clocks.game else pygame.mixer.music.get_pos()
        self.transformations["colorFade"][
            "endTime"] = time.time() * 1000 + duration if self.Clock == Clocks.game else pygame.mixer.music.get_pos() + duration
        self.transformations["colorFade"]["beginValue"] = self.color
        self.transformations["colorFade"]["endValue"] = color
        self.transformations["colorFade"]["easing"] = easing
        self.transformations["colorFade"]["loop"] = loop

    def VectorScaleTo(self, scale, duration, easing=EaseTypes.linear,
                      loop=False):
        self.transformations["VectorScale"][
            "beginTime"] = time.time() * 1000 if self.Clock == Clocks.game else pygame.mixer.music.get_pos()
        self.transformations["VectorScale"][
            "endTime"] = time.time() * 1000 + duration if self.Clock == Clocks.game else pygame.mixer.music.get_pos() + duration
        self.transformations["VectorScale"]["beginValue"] = self.vectorScale
        self.transformations["VectorScale"]["endValue"] = scale
        self.transformations["VectorScale"]["easing"] = easing
        self.transformations["VectorScale"]["loop"] = loop

    def ScaleTo(self, scale, duration, easing=EaseTypes.linear, loop=False):
        self.transformations["scale"][
            "beginTime"] = time.time() * 1000 if self.Clock == Clocks.game else pygame.mixer.music.get_pos()
        self.transformations["scale"][
            "endTime"] = time.time() * 1000 + duration if self.Clock == Clocks.game else pygame.mixer.music.get_pos() + duration
        self.transformations["scale"]["beginValue"] = self.scale
        self.transformations["scale"]["endValue"] = scale
        self.transformations["scale"]["easing"] = easing
        self.transformations["scale"]["loop"] = loop

    def ClearTransformations(self, type=None):
        self.transformations = {"scale": {}, "fade": {}, "VectorScale": {},
                                "position": {}, "colorFade": {},
                                "rotation": {}}

    def UpdateStats(self, init=False):
        if self.field == Positions.topLeft:
            self.offset = vector2(0, 0)
        elif self.field == Positions.topCentre:
            self.offset = vector2(CONST.windowManager.width / 2, 0)
        elif self.field == Positions.topRight:
            self.offset = vector2(CONST.windowManager.width, 0)
            if init:
                self.posMult = -1
        elif self.field == Positions.centreLeft:
            self.offset = vector2(0, CONST.windowManager.height / 2)
        elif self.field == Positions.centre:
            self.offset = vector2(CONST.windowManager.width / 2,
                                  CONST.windowManager.height / 2)
        elif self.field == Positions.centreRight:
            self.offset = vector2(CONST.windowManager.width,
                                  CONST.windowManager.height / 2)
            if init:
                self.posMult = -1
        elif self.field == Positions.bottomLeft:
            self.offset = vector2(0, CONST.windowManager.height)
            self.posMultY = -1
        elif self.field == Positions.bottomCentre:
            self.offset = vector2(CONST.windowManager.width / 2,
                                  CONST.windowManager.height)
            if init:
                self.posMultY = -1
        elif self.field == Positions.bottomRight:
            self.offset = vector2(CONST.windowManager.width,
                                  CONST.windowManager.height)
            if init:
                self.posMultY = -1
                self.posMult = -1
        width = self.image.get_width()
        height = self.image.get_height()
        if self.origin == Positions.topCentre:
            self.offset.x -= width / 2
        elif self.origin == Positions.topRight:
            self.offset.x -= width
        elif self.origin == Positions.centreLeft:
            self.offset.y -= height / 2
        elif self.origin == Positions.centre:
            self.offset.x -= width / 2
            self.offset.y -= height / 2
        elif self.origin == Positions.centreRight:
            self.offset.x -= width
            self.offset.y -= height / 2
        elif self.origin == Positions.bottomLeft:
            self.offset.y -= height
        elif self.origin == Positions.bottomCentre:
            self.offset.x -= width / 2
            self.offset.y -= height
        elif self.origin == Positions.bottomRight:
            self.offset.x -= width
            self.offset.y -= height
        self.effectivePosition = vector2(self.offset.x, self.offset.y)

    def draw(self):
        if self.enabled:
            beginRect = vector2((
                    self.effectivePosition.x + CONST.windowManager.getPixelSize() *
                    ((
                             self.originPosition.x + self.position.x) * self.posMult)),
                self.effectivePosition.y + CONST.windowManager.getPixelSize() *
                ((self.originPosition.y + self.position.y) * self.posMultY))
            endRect = vector2(
                beginRect.x + (self.image.get_width()),
                beginRect.y + (self.image.get_height())
            )
            actuallyHover = (
                                    CONST.cursorPos.x > beginRect.x and CONST.cursorPos.x < endRect.x) and (
                                    CONST.cursorPos.y > beginRect.y and CONST.cursorPos.y < endRect.y) and self.alpha > 0
            if actuallyHover and not self.isonHover:
                self.isonHover = True
                self.__onHover__()
            elif not actuallyHover and self.isonHover:
                self.isonHover = False
                self.__onHoverLost__()

            if self.Clock == Clocks.game:
                now = time.time() * 1000
            else:
                now = pygame.mixer.music.get_pos()

            if self.transformations["rotation"] != {}:
                beginTime = self.transformations["rotation"]["beginTime"]
                endtime = self.transformations["rotation"]["endTime"]
                beginValue = self.transformations["rotation"]["beginValue"]
                endValue = self.transformations["rotation"]["endValue"]
                easing = self.transformations["rotation"]["easing"]
                if self.scale == endValue:
                    if self.transformations["rotation"]["loop"]:
                        duration = self.transformations["rotation"][
                                       "endTime"] - \
                                   self.transformations["rotation"][
                                       "beginTime"]
                        self.transformations["rotation"]["beginTime"] = now
                        self.transformations["rotation"][
                            "endTime"] = now + duration
                        self.transformations["rotation"][
                            "beginValue"] = endValue
                        self.transformations["rotation"][
                            "endValue"] = beginValue
                    else:
                        self.transformations["rotation"] = {}
                elif now > beginTime:
                    self.Scale(self.scale)
                    if self.Clock == Clocks.game:
                        self.Rotate(
                            helper.getTimeValue(beginTime, endtime, beginValue,
                                                endValue, easing))
                    else:
                        self.Rotate(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValue, endValue,
                                                     easing))

            if self.transformations["scale"] != {}:
                beginTime = self.transformations["scale"]["beginTime"]
                endtime = self.transformations["scale"]["endTime"]
                beginValue = self.transformations["scale"]["beginValue"]
                endValue = self.transformations["scale"]["endValue"]
                easing = self.transformations["scale"]["easing"]
                if self.scale == endValue:
                    if self.transformations["scale"]["loop"]:
                        duration = self.transformations["scale"]["endTime"] - \
                                   self.transformations["scale"][
                                       "beginTime"]
                        self.transformations["scale"]["beginTime"] = now
                        self.transformations["scale"][
                            "endTime"] = now + duration
                        self.transformations["scale"]["beginValue"] = endValue
                        self.transformations["scale"]["endValue"] = beginValue
                    else:
                        self.transformations["scale"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Scale(
                            helper.getTimeValue(beginTime, endtime, beginValue,
                                                endValue, easing))
                    else:
                        self.Scale(helper.getAudioTimeValue(beginTime, endtime,
                                                            beginValue,
                                                            endValue, easing))

            if self.transformations["fade"] != {}:
                beginTime = self.transformations["fade"]["beginTime"]
                endtime = self.transformations["fade"]["endTime"]
                beginValue = self.transformations["fade"]["beginValue"]
                endValue = self.transformations["fade"]["endValue"]
                easing = self.transformations["fade"]["easing"]
                if self.alpha == endValue:
                    if self.transformations["fade"]["loop"]:
                        duration = self.transformations["fade"]["endTime"] - \
                                   self.transformations["fade"]["beginTime"]
                        self.transformations["fade"]["beginTime"] = now
                        self.transformations["fade"][
                            "endTime"] = now + duration
                        self.transformations["fade"]["beginValue"] = endValue
                        self.transformations["fade"]["endValue"] = beginValue
                    else:
                        self.transformations["fade"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Fade(
                            helper.getTimeValue(beginTime, endtime, beginValue,
                                                endValue, easing))
                    else:
                        self.Fade(helper.getAudioTimeValue(beginTime, endtime,
                                                           beginValue,
                                                           endValue, easing))
            if self.transformations["VectorScale"] != {}:
                beginTime = self.transformations["VectorScale"]["beginTime"]
                endtime = self.transformations["VectorScale"]["endTime"]
                beginValueX = self.transformations["VectorScale"][
                    "beginValue"].x
                endValueX = self.transformations["VectorScale"]["endValue"].x
                beginValueY = self.transformations["VectorScale"][
                    "beginValue"].y
                endValueY = self.transformations["VectorScale"]["endValue"].y
                easing = self.transformations["VectorScale"]["easing"]
                if self.vectorScale.x == endValueX and self.vectorScale.y == endValueY:
                    if self.transformations["VectorScale"]["loop"]:
                        duration = self.transformations["VectorScale"][
                                       "endTime"] - \
                                   self.transformations["VectorScale"][
                                       "beginTime"]
                        self.transformations["VectorScale"]["beginTime"] = now
                        self.transformations["VectorScale"][
                            "endTime"] = now + duration
                        self.transformations["VectorScale"][
                            "beginValue"] = vector2(endValueX, endValueY)
                        self.transformations["VectorScale"][
                            "endValue"] = vector2(beginValueX, beginValueY)
                    else:
                        self.transformations["VectorScale"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.VectorScale(vector2(
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueX, endValueX,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueY, endValueY,
                                                easing)))
                    else:
                        self.VectorScale(vector2(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueX, endValueX,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueY, endValueY,
                                                     easing)))

            if self.transformations["colorFade"] != {}:
                beginTime = self.transformations["colorFade"]["beginTime"]
                endtime = self.transformations["colorFade"]["endTime"]

                beginValueR = self.transformations["colorFade"]["beginValue"].r
                endValueR = self.transformations["colorFade"]["endValue"].r

                beginValueG = self.transformations["colorFade"]["beginValue"].g
                endValueG = self.transformations["colorFade"]["endValue"].g

                beginValueB = self.transformations["colorFade"]["beginValue"].b
                endValueB = self.transformations["colorFade"]["endValue"].b

                easing = self.transformations["colorFade"]["easing"]
                if self.color.r == endValueR and self.color.g == endValueG and self.color.b == endValueB:
                    if self.transformations["colorFade"]["loop"]:
                        duration = self.transformations["colorFade"][
                                       "endTime"] - \
                                   self.transformations["colorFade"][
                                       "beginTime"]
                        self.transformations["colorFade"]["beginTime"] = now
                        self.transformations["colorFade"][
                            "endTime"] = now + duration
                        self.transformations["colorFade"][
                            "beginValue"] = Color(endValueR, endValueG,
                                                  endValueB)
                        self.transformations["colorFade"]["endValue"] = Color(
                            beginValueR, beginValueG, beginValueB)
                    else:
                        self.transformations["colorFade"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.Color(Color(
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueR, endValueR,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueG, endValueG,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueB, endValueB,
                                                easing)))
                    else:
                        self.Color(Color(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueR, endValueR,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueG, endValueG,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueB, endValueB,
                                                     easing)))

            if self.transformations["position"] != {}:
                beginTime = self.transformations["position"]["beginTime"]
                endtime = self.transformations["position"]["endTime"]
                beginValueX = self.transformations["position"]["beginValue"].x
                endValueX = self.transformations["position"]["endValue"].x
                beginValueY = self.transformations["position"]["beginValue"].y
                endValueY = self.transformations["position"]["endValue"].y
                easing = self.transformations["position"]["easing"]
                if self.position.x == endValueX and self.position.y == endValueY:
                    if self.transformations["position"]["loop"]:
                        duration = self.transformations["position"][
                                       "endTime"] - \
                                   self.transformations["position"][
                                       "beginTime"]
                        self.transformations["position"]["beginTime"] = now
                        self.transformations["position"][
                            "endTime"] = now + duration
                        self.transformations["position"][
                            "beginValue"] = vector2(endValueX, endValueY)
                        self.transformations["position"]["endValue"] = vector2(
                            beginValueX, beginValueY)
                    else:
                        self.transformations["position"] = {}
                elif now > beginTime:
                    if self.Clock == Clocks.game:
                        self.position = vector2(
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueX, endValueX,
                                                easing),
                            helper.getTimeValue(beginTime, endtime,
                                                beginValueY, endValueY,
                                                easing))
                    else:
                        self.position = vector2(
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueX, endValueX,
                                                     easing),
                            helper.getAudioTimeValue(beginTime, endtime,
                                                     beginValueY, endValueY,
                                                     easing))
        self.UpdateStats()
        if self.alpha != 0:
            CONST.surface.blit(self.image,
                               (
                                   self.effectivePosition.x + CONST.windowManager.getPixelSize() *
                                   ((
                                            self.originPosition.x + self.position.x) * self.posMult),
                                   self.effectivePosition.y + CONST.windowManager.getPixelSize() *
                                   ((
                                            self.originPosition.y + self.position.y) * self.posMultY)))
