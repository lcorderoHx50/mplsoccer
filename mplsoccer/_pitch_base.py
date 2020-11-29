import warnings
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

from mplsoccer import dimensions
from mplsoccer.cm import grass_cmap


class BasePitch(ABC):
    """ A class for plotting soccer / football pitches in Matplotlib

    Parameters
    ----------
    figsize : tuple of float, default Matplotlib figure size
        The figure size in inches by default.
    nrows, ncols : int, default 1
        Number of rows/columns of the subplot grid.
    pitch_type : str, default 'statsbomb'
        The pitch type used in the plot.
        The supported pitch types are: 'opta', 'statsbomb', 'tracab',
        'wyscout', 'uefa', 'metricasports', 'custom'.
    half : bool, default False
        Whether to display half of the pitch.
    pitch_color : any Matplotlib color, default None
        The background color for each Matplotlib axis. If None, defaults to rcParams["axes.facecolor"].
        To remove the background set to "None" or 'None'.
    line_color : any Matplotlib color, default None
        The line color for the pitch markings. If None, defaults to rcParams["grid.color"].
    line_zorder : float, default 0.9
        Set the zorder for the pitch lines (a matplotlib artist). Artists with lower zorder values are drawn first.
    linewidth : float, default 2
        The line width for the pitch markings.
    spot_scale : float, default 0.002
        The size of the penalty and center spots relative to the pitch length.
    stripe : bool, default False
        Whether to show pitch stripes.
    stripe_color : any Matplotlib color, default '#c2d59d'
        The color of the pitch stripes if stripe=True
    stripe_zorder : float, default 0.6
        Set the zorder for the stripes (a matplotlib artist). Artists with lower zorder values are drawn first.
    pad_left : float, default None
        Adjusts the left xlim of the axis. Positive values increase the plot area,
        while negative values decrease the plot area.
        If None set to 0.04 for 'metricasports' pitch and 4 otherwise.
    pad_right : float, default None
        Adjusts the right xlim of the axis. Positive values increase the plot area,
        while negative values decrease the plot area.
        If None set to 0.04 for 'metricasports' pitch and 4 otherwise.
    pad_bottom : float, default None
        Adjusts the bottom ylim of the axis. Positive values increase the plot area,
        while negative values decrease the plot area.
        If None set to 0.04 for 'metricasports' pitch and 4 otherwise.
    pad_top : float, default None
        Adjusts the top ylim of the axis. Positive values increase the plot area,
        while negative values decrease the plot area.
        If None set to 0.04 for 'metricasports' pitch and 4 otherwise.
    positional : bool, default False
        Whether to draw Juego de Posición lines.
    positional_zorder : float, default 0.8
        Set the zorder for the Juego de Posición lines. Artists with lower zorder values are drawn first.
    positional_linewidth : float, default None
        Linewidth for the Juego de Posición lines.
        If None then this defaults to the same linewidth as the pitch lines (linewidth).
    positional_linestyle : str or tuple
        Linestyle for the Juego de Posición lines: {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
        see: https://matplotlib.org/3.2.1/gallery/lines_bars_and_markers/linestyles.html
    positional_color : any Matplotlib color, default '#eadddd'
        The line color for the Juego de Posición lines.
    shade_middle : bool, default False
         Whether to shade the middle third of the pitch.
    shade_color : any Matplotlib color, default '#f2f2f2'
        The fill color for the shading of the middle third of the pitch.
    shade_zorder : float, default 0.7
        Set the zorder for the shading of the middle third of the pitch.
        Artists with lower zorder values are drawn first.
    pitch_length : float, default None
        The pitch length in meters. Only used for the 'tracab' and 'metricasports' pitch_type.
    pitch_width : float, default None
        The pitch width in meters. Only used for the 'tracab' and 'metricasports' pitch type.
    goal_type : str, default 'line'
        Whether to display the goals as a 'line', a 'box' or to not display it at all (None)
    axis : bool, default False
        Whether to include the axis: True means the axis is 'on' and False means the axis is 'off'.
    label : bool, default False
        Whether to include the axis labels.
    tick : bool, default False
        Whether to include the axis ticks.
    tight_layout : bool, default True
        Whether to use Matplotlib's tight layout.
    constrained_layout : bool, default False
        Whether to use Matplotlib's constrained layout.
    """

    def __init__(self, figsize=None, nrows=1, ncols=1, pitch_type='statsbomb', half=False,
                 pitch_color=None, line_color=None, linewidth=2, line_zorder=0.9, stripe=False,
                 stripe_color='#c2d59d', stripe_zorder=0.6, pad_left=None, pad_right=None, pad_bottom=None,
                 pad_top=None,
                 positional=False, positional_zorder=0.8, positional_linewidth=None,
                 positional_linestyle=None, positional_color='#eadddd',
                 shade_middle=False, shade_color='#f2f2f2', shade_zorder=0.7,
                 pitch_length=None, pitch_width=None, goal_type='line', label=False, tick=False, axis=False,
                 tight_layout=True, constrained_layout=False, spot_scale=0.002):

        # validate the pitch_type and for pitches where the size varies check they have a pitch_length/width
        if pitch_type not in dimensions.valid:
            raise TypeError(f'Invalid argument: pitch_type should be in {dimensions.valid}')
        if (pitch_length is None or pitch_width is None) and pitch_type in dimensions.size_varies:
            raise TypeError("Invalid argument: pitch_length and pitch_width must be specified.")
        if ((pitch_type not in dimensions.size_varies) and
                ((pitch_length is not None) or (pitch_width is not None))):
            warnings.warn(
                f"Pitch length and widths are only used for {dimensions.size_varies} pitches and will be ignored")

        self.axes = None
        self.fig = None
        self.figsize = figsize
        self.nrows = nrows
        self.ncols = ncols
        self.pitch_type = pitch_type
        self.half = half
        self.pitch_color = pitch_color
        if self.pitch_color is None:
            self.pitch_color = rcParams['axes.facecolor']
        self.line_color = line_color
        if self.line_color is None:
            self.line_color = rcParams["grid.color"]
        self.linewidth = linewidth
        self.line_zorder = line_zorder
        self.stripe = stripe
        self.stripe_color = stripe_color
        self.stripe_zorder = stripe_zorder
        self.pad_left = pad_left
        self.pad_right = pad_right
        self.pad_bottom = pad_bottom
        self.pad_top = pad_top
        self.positional = positional
        self.positional_zorder = positional_zorder
        self.positional_linewidth = positional_linewidth
        if self.positional_linewidth is None:
            self.positional_linewidth = linewidth
        self.positional_linestyle = positional_linestyle
        self.positional_color = positional_color
        self.shade_middle = shade_middle
        self.shade_color = shade_color
        self.shade_zorder = shade_zorder
        self.pitch_length = pitch_length
        self.pitch_width = pitch_width
        self.goal_type = goal_type
        self.label = label
        self.tick = tick
        self.axis = axis
        self.tight_layout = tight_layout
        self.constrained_layout = constrained_layout
        self.spot_scale = spot_scale

        # if the padding is None set it to 4 on all sides, or 0.04 in the case of metricasports
        for pad in ['pad_left', 'pad_right', 'pad_bottom', 'pad_top']:
            if getattr(self, pad) is None:
                if pitch_type != 'metricasports':
                    setattr(self, pad, 4)
                else:
                    setattr(self, pad, 0.04)

        # set the dimensions for individual pitch_type(s)
        if pitch_type == 'opta':
            self._set_dimensions(dimensions.opta)
            self.pitch_length = 105
            self.pitch_width = 68

        elif pitch_type == 'wyscout':
            self._set_dimensions(dimensions.wyscout)
            self.pitch_length = 105
            self.pitch_width = 68

        elif pitch_type == 'statsbomb':
            self._set_dimensions(dimensions.statsbomb)
            self.pitch_length = self.length
            self.pitch_width = self.width

        elif pitch_type == 'uefa':
            self._set_dimensions(dimensions.uefa)
            self.pitch_length = self.length
            self.pitch_width = self.width

        elif pitch_type == 'tracab':
            self._set_dimensions(dimensions.tracab)
            self.top = pitch_width / 2 * 100
            self.bottom = -(pitch_width / 2) * 100
            self.left = -(pitch_length / 2) * 100
            self.right = (pitch_length / 2) * 100
            self.width = pitch_width * 100
            self.length = pitch_length * 100
            self.left_penalty = self.left + 1100
            self.right_penalty = self.right - 1100
            self.pad_left = self.pad_left * 100
            self.pad_bottom = self.pad_bottom * 100
            self.pad_right = self.pad_right * 100
            self.pad_top = self.pad_top * 100

        elif pitch_type == 'metricasports':
            # note do not scale the circle_size as scaled seperately for the width/ length when drawing circle/arcs
            self._set_dimensions(dimensions.metricasports)
            self.aspect = self.pitch_width / self.pitch_length
            self.six_yard_width = round(self.six_yard_width / self.pitch_width, 4)
            self.six_yard_length = round(self.six_yard_length / self.pitch_length, 4)
            self.six_yard_from_side = (self.width - self.six_yard_width) / 2
            self.penalty_area_width = round(self.penalty_area_width / self.pitch_width, 4)
            self.penalty_area_length = round(self.penalty_area_length / self.pitch_length, 4)
            self.penalty_area_from_side = (self.width - self.penalty_area_width) / 2
            self.left_penalty = round(self.left_penalty / self.pitch_length, 4)
            self.right_penalty = self.right - self.left_penalty
            self.goal_depth = round(self.goal_depth / self.pitch_length, 4)
            self.goal_width = round(self.goal_width / self.pitch_width, 4)
            self.goal_post = self.center_width - round(self.goal_post / self.pitch_width, 4)

        elif pitch_type == 'custom':
            self._set_dimensions(dimensions.custom)
            self.right = self.pitch_length
            self.top = self.pitch_width
            self.length = self.pitch_length
            self.width = self.pitch_width
            self.center_length = self.pitch_length / 2
            self.center_width = self.pitch_width / 2
            self.six_yard_from_side = self.center_width - self.six_yard_width / 2
            self.penalty_area_from_side = self.center_width - self.penalty_area_width / 2
            self.right_penalty = self.right - self.left_penalty
            self.goal_post = self.center_width - self.goal_width / 2

        elif pitch_type == 'skillcorner':
            self._set_dimensions(dimensions.skillcorner)
            self.top = pitch_width / 2
            self.bottom = -(pitch_width / 2)
            self.left = -(pitch_length / 2)
            self.right = (pitch_length / 2)
            self.width = pitch_width
            self.length = pitch_length
            self.left_penalty = self.left + 11
            self.right_penalty = self.right - 11
        
        # scale the padding where the aspect is not equal to one
        # this means that you can easily set the padding the same all around the pitch (e.g. when using an Opta pitch)
        if self.aspect != 1:
            self._scale_pad()

        # set the pitch_extent: [xmin, xmax, ymin, ymax]
        self.pitch_extent = np.array([min(self.left, self.right), max(self.left, self.right),
                                      min(self.bottom, self.top), max(self.bottom, self.top)])
        
        # set the extent (takes into account padding) [xleft, xright, ybottom, ytop] and the aspect ratio of the axis
        self._set_extent()
        self.ax_aspect = abs(self.extent[0] - self.extent[1]) / abs(self.extent[2] - self.extent[3]) * self.aspect
        
        # data checks
        self._validation_checks()
        self._validate_pad()

        # positions of the Juego de Posición lines and stripe locations
        self._juego_de_posicion()
        self._stripe_locations()

        # calculate locations of arcs and circles.
        # Where the pitch has an unequal aspect ratio we need to do this seperately
        if (self.aspect == 1) and (self.pitch_type != 'metricasports'):
            self._init_circles_and_arcs()

        # set the positions of the goal posts
        self.goal_right = np.array([[self.right, self.center_width - self.goal_width / 2],
                                    [self.right, self.center_width + self.goal_width / 2]])
        self.goal_left = np.array([[self.left, self.center_width - self.goal_width / 2],
                                   [self.left, self.center_width + self.goal_width / 2]])

    def _set_dimensions(self, pitch_dimensions):
        for key, value in pitch_dimensions.items():
            setattr(self, key, value)

    def _scale_pad(self):
        self.pad_left = self.pad_left * self.aspect
        self.pad_right = self.pad_right * self.aspect

    def _validation_checks(self):
        for attribute in ['axis', 'stripe', 'tick', 'label', 'shade_middle', 'tight_layout',
                          'half', 'positional', 'constrained_layout']:
            if not isinstance(getattr(self, attribute), bool):
                raise TypeError(f"Invalid argument: '{attribute}' should be bool.")
        if (self.axis is False) and self.label:
            warnings.warn("Labels will not be shown unless axis=True")
        if (self.axis is False) and self.tick:
            warnings.warn("Ticks will not be shown unless axis=True")
        valid_goal_type = ['line', 'box']
        if self.goal_type not in valid_goal_type:
            raise TypeError(f'Invalid argument: goal_type should be in {valid_goal_type}')

    def _validate_pad(self):
        # make sure padding not too large for the pitch
        if abs(min(self.pad_left, 0) + min(self.pad_right, 0)) >= self.length:
            raise ValueError("pad_left/pad_right too negative for pitch length")
        if abs(min(self.pad_top, 0) + min(self.pad_bottom, 0)) >= self.width:
            raise ValueError("pad_top/pad_bottom too negative for pitch width")
        if self.half:
            if abs(min(self.pad_left, 0) + min(self.pad_right, 0)) >= self.length / 2:
                raise ValueError("pad_left/pad_right too negative for pitch length")

    def _juego_de_posicion(self):
        # x positions for Juego de Posición
        self.x1 = min(self.left, self.right)
        self.x4 = self.center_length
        self.x7 = max(self.left, self.right)
        self.x2 = self.x1 + self.penalty_area_length
        self.x6 = self.x7 - self.penalty_area_length
        self.x3 = self.x2 + (self.x4 - self.x2) / 2
        self.x5 = self.x4 + (self.x6 - self.x4) / 2

        # y positions for Juego de Posición
        self.y1 = min(self.bottom, self.top)
        self.y6 = max(self.bottom, self.top)
        if self.origin_center:
            self.y2 = self.penalty_area_from_side
            self.y3 = self.six_yard_from_side
            self.y4 = -self.six_yard_from_side
            self.y5 = -self.penalty_area_from_side
        else:
            self.y3 = self.y1 + self.six_yard_from_side
            self.y2 = self.y1 + self.penalty_area_from_side
            self.y4 = self.y6 - self.six_yard_from_side
            self.y5 = self.y6 - self.penalty_area_from_side
            self.y4 = self.y6 - self.six_yard_from_side

    def _stripe_locations(self):
        stripe_six_yard = self.six_yard_length
        stripe_pen_area = (self.penalty_area_length - self.six_yard_length) / 2
        stripe_other = (self.right - self.left -
                        (self.penalty_area_length - self.six_yard_length) * 3 - self.six_yard_length * 2) / 10
        stripe_locations = ([self.left] + [stripe_six_yard] + [stripe_pen_area] * 3 +
                            [stripe_other] * 10 + [stripe_pen_area] * 3 + [stripe_six_yard])
        self.stripe_locations = np.array(stripe_locations).cumsum()

    def _init_circles_and_arcs(self):
        self.diameter1 = self.circle_diameter
        self.diameter2 = self.circle_diameter
        self.size_spot1 = self.spot_scale * self.length * 2  # *2 as elipse uses diameter rather than radius
        self.size_spot2 = self.spot_scale * self.length * 2  # *2 as elipse uses diameter rather than radius
        self.arc1_theta1 = -self.arc
        self.arc1_theta2 = self.arc
        self.arc2_theta1 = 180 - self.arc
        self.arc2_theta2 = 180 + self.arc

    def _init_circles_and_arcs_equal_aspect(self, ax):
        r1 = self.circle_diameter / 2 * self.width / self.pitch_width
        r2 = self.circle_diameter / 2 * self.length / self.pitch_length
        size_spot = self.spot_scale * self.pitch_length
        scaled_spot1 = size_spot * self.width / self.pitch_width
        scaled_spot2 = size_spot * self.length / self.pitch_length
        xy = (self.center_width, self.center_length)
        intersection = self.center_width - (
                r1 * r2 * (r2 ** 2 - (self.penalty_area_length - self.left_penalty) ** 2) ** 0.5) / (r2 ** 2)

        xy1 = (self.center_width + r2, self.center_length)
        xy2 = (self.center_width, self.center_length + r1)
        spot1 = (self.left_penalty, self.center_width)
        spot2 = (self.right_penalty, self.center_width)
        center_spot = (self.center_length, self.center_width)
        p2 = (self.left_penalty, self.center_width + scaled_spot1)
        p1 = (self.left_penalty + scaled_spot2, self.center_width)
        arc_pen_top1 = (self.penalty_area_length, intersection)

        ax_coordinate_system = ax.transAxes
        coord_name = ['xy', 'spot1', 'spot2', 'center', 'xy1', 'xy2', 'p1', 'p2', 'arc_pen_top1']
        coord_dict = {}
        for i, coord in enumerate([xy, spot1, spot2, center_spot, xy1, xy2, p1, p2, arc_pen_top1]):
            coord_dict[coord_name[i]] = self._to_ax_coord(ax, ax_coordinate_system, coord)

        self.center = coord_dict['center']
        self.penalty1 = coord_dict['spot1']
        self.penalty2 = coord_dict['spot2']
        self.diameter1 = (coord_dict['xy1'][0] - coord_dict['xy'][0]) * 2
        self.diameter2 = (coord_dict['xy2'][1] - coord_dict['xy'][1]) * 2
        self.size_spot1 = (coord_dict['p1'][0] - coord_dict['spot1'][0]) * 2
        self.size_spot2 = (coord_dict['p2'][1] - coord_dict['spot1'][1]) * 2

        a = coord_dict['arc_pen_top1'][0] - coord_dict['spot1'][0]
        o = coord_dict['spot1'][1] - coord_dict['arc_pen_top1'][1]

        self.arc1_theta2 = np.degrees(np.arctan(o / a))
        self.arc1_theta1 = 360 - self.arc1_theta2
        self.arc2_theta1 = 180 - self.arc1_theta2
        self.arc2_theta2 = 180 + self.arc1_theta2

    @staticmethod
    def _to_ax_coord(ax, coord_system, point):
        return coord_system.inverted().transform(ax.transData.transform_point(point))

    def draw(self, ax=None):
        """ Draws the specified soccer/ football pitch(es).
        If an ax is specified the pitch is drawn on an existing axis.

        Parameters
        ----------
        ax : matplotlib axis, default None
            A matplotlib.axes.Axes to draw the pitch on. If None is specified the pitch is plotted on a new figure.

        Returns
        -------
        If ax=None returns a matplotlib Figure and Axes.
        Else plotted on an existing axis and returns None.

        Examples
        --------
        # plot on new figure
        pitch = Pitch()
        fig, ax = pitch.draw()

        # plot on an existing figure
        fig, ax = plt.subplots()
        pitch = Pitch()
        pitch.draw(ax=ax)
        """
        if ax is None:
            self._setup_subplots()
            self.fig.set_tight_layout(self.tight_layout)
            if hasattr(self, 'arc1_theta1') is False:
                self._init_circles_and_arcs_equal_aspect(self.axes.flat[0])
            for ax in self.axes.flat:
                self._draw_ax(ax)
            if self.axes.size == 1:
                self.axes = self.axes.item()
            return self.fig, self.axes

        else:
            if hasattr(self, 'arc1_theta1') is False:
                self._init_circles_and_arcs_equal_aspect(ax)
            self._draw_ax(ax)

    def _setup_subplots(self):
        fig, axes = plt.subplots(nrows=self.nrows, ncols=self.ncols, figsize=self.figsize,
                                 constrained_layout=self.constrained_layout)
        if (self.nrows == 1) and (self.ncols == 1):
            axes = np.array([axes])
        self.fig = fig
        self.axes = axes

    def _draw_ax(self, ax):
        self._set_axes(ax)
        self._set_background(ax)
        self._draw_pitch_markings(ax)
        self._draw_goals(ax)
        if self.positional:
            self._draw_juego_de_posicion(ax)
        if self.shade_middle:
            self._draw_shade_middle(ax)

    def _set_axes(self, ax):
        # set axis on/off, and labels and ticks
        if self.axis is False:
            ax.spines['bottom'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['right'].set_visible(False)
        ax.grid(False)
        ax.tick_params(top=self.tick, bottom=self.tick, left=self.tick, right=self.tick,
                       labelleft=self.label, labelbottom=self.label)
        # set limits and aspect
        ax.set_xlim(self.extent[0], self.extent[1])
        ax.set_ylim(self.extent[2], self.extent[3])
        ax.set_aspect(self.aspect)

    def _set_background(self, ax):
        if self.pitch_color != 'grass':
            ax.set_facecolor(self.pitch_color)
            if self.stripe:
                self._plain_stripes(ax)
        else:
            pitch_color = np.random.normal(size=(1000, 1000))
            if self.stripe:
                pitch_color = self._draw_stripe_grass(pitch_color)
            ax.imshow(pitch_color, cmap=grass_cmap(), extent=self.extent, aspect=self.aspect)
    
    def _plain_stripes(self, ax):
        for i in range(len(self.stripe_locations) - 1):
            if i % 2 == 0:
                self._draw_stripe(ax, i)

    def _draw_pitch_markings(self, ax):
        rect_prop = {'fill': False, 'linewidth': self.linewidth, 'color': self.line_color, 'zorder': self.line_zorder}
        line_prop = {'linewidth': self.linewidth, 'color': self.line_color, 'zorder': self.line_zorder}
        # penalty boxes and six-yard boxes
        self._draw_rectangle(ax, self.left, self.six_yard_from_side,
                             self.six_yard_length, self.six_yard_width, **rect_prop)
        self._draw_rectangle(ax, self.right - self.six_yard_length, self.six_yard_from_side,
                             self.six_yard_length, self.six_yard_width, **rect_prop)
        self._draw_rectangle(ax, self.left, self.penalty_area_from_side,
                             self.penalty_area_length, self.penalty_area_width, **rect_prop)
        self._draw_rectangle(ax, self.right - self.penalty_area_length, self.penalty_area_from_side,
                             self.penalty_area_length, self.penalty_area_width, **rect_prop)
        # pitch
        self._draw_rectangle(ax, self.left, self.pitch_extent[2], self.length, self.width, **rect_prop)
        # mid-line
        self._draw_line(ax, [self.center_length, self.center_length], [self.bottom, self.top], **line_prop)
        # circles and arcs
        self._draw_circles_and_arcs(ax)

    def _draw_circles_and_arcs(self, ax):
        circ_prop = {'fill': False, 'linewidth': self.linewidth, 'color': self.line_color, 'zorder': self.line_zorder}

        # draw center cicrle and penalty area arcs
        self._draw_ellipse(ax, self.center_length, self.center_width, self.diameter1, self.diameter2, **circ_prop)
        self._draw_arc(ax, self.left_penalty, self.center_width, self.diameter1, self.diameter2,
                       theta1=self.arc1_theta1, theta2=self.arc1_theta2, **circ_prop)
        self._draw_arc(ax, self.right_penalty, self.center_width, self.diameter1, self.diameter2,
                       theta1=self.arc2_theta1, theta2=self.arc2_theta2, **circ_prop)

        # draw center and penalty spots
        if self.spot_scale > 0:
            self._draw_ellipse(ax, self.center_length, self.center_width,
                               self.size_spot1, self.size_spot2, color=self.line_color, zorder=self.line_zorder)
            self._draw_ellipse(ax, self.left_penalty, self.center_width,
                               self.size_spot1, self.size_spot2, color=self.line_color, zorder=self.line_zorder)
            self._draw_ellipse(ax, self.right_penalty, self.center_width,
                               self.size_spot1, self.size_spot2, color=self.line_color, zorder=self.line_zorder)

    def _draw_goals(self, ax):
        rect_prop = {'fill': False, 'linewidth': self.linewidth, 'color': self.line_color, 'alpha': 0.7,
                     'zorder': self.line_zorder}
        line_prop = {'linewidth': self.linewidth * 2, 'color': self.line_color, 'zorder': self.line_zorder}
        if self.goal_type == 'box':
            self._draw_rectangle(ax, self.right, self.goal_post, self.goal_depth, self.goal_width, **rect_prop)
            self._draw_rectangle(ax, self.left - self.goal_depth,
                                 self.goal_post, self.goal_depth, self.goal_width, **rect_prop)

        elif self.goal_type == 'line':
            self._draw_line(ax, [self.right, self.right], [self.goal_post + self.goal_width, self.goal_post],
                            **line_prop)
            self._draw_line(ax, [self.left, self.left], [self.goal_post + self.goal_width, self.goal_post], **line_prop)

    def _draw_juego_de_posicion(self, ax):
        line_prop = {'linewidth': self.positional_linewidth, 'color': self.positional_color,
                     'linestyle': self.positional_linestyle, 'zorder': self.positional_zorder}
        # x lines for Juego de Posición
        for coord in [self.x2, self.x3, self.x4, self.x5, self.x6]:
            self._draw_line(ax, [coord, coord], [self.bottom, self.top], **line_prop)
        # y lines for Juego de Posición
        self._draw_line(ax, [self.left, self.right], [self.y2, self.y2], **line_prop)
        self._draw_line(ax, [self.left, self.right], [self.y5, self.y5], **line_prop)
        self._draw_line(ax, [self.left + self.penalty_area_length, self.right - self.penalty_area_length],
                        [self.y3, self.y3], **line_prop)
        self._draw_line(ax, [self.left + self.penalty_area_length, self.right - self.penalty_area_length],
                        [self.y4, self.y4], **line_prop)

    def _draw_shade_middle(self, ax):
        shade_prop = {'fill': True, 'facecolor': self.shade_color, 'zorder': self.shade_zorder}
        self._draw_rectangle(ax, self.x3, self.pitch_extent[2], self.x5 - self.x3, self.width, **shade_prop)

    @abstractmethod
    def _set_extent(self):
        pass

    @abstractmethod
    def _draw_rectangle(self, ax, x, y, width, height, **kwargs):
        pass

    @abstractmethod
    def _draw_line(self, ax, x, y, **kwargs):
        pass

    @abstractmethod
    def _draw_ellipse(self, ax, x, y, width, height, **kwargs):
        pass

    @abstractmethod
    def _draw_arc(self, ax, x, y, width, height, theta1, theta2, **kwargs):
        pass
    
    @abstractmethod
    def _draw_stripe(self, ax, i):
        pass
