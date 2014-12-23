(function($){

    $.fn.hitTest = function(x, y){
        var bounds = this.offset();
        bounds.right = bounds.left + this.outerWidth();
        bounds.bottom = bounds.top + this.outerHeight();
        if(x >= bounds.left){
            if(x <= bounds.right){
                if(y >= bounds.top){
                    if(y <= bounds.bottom){
                        return true;
                    }
                }
            }
        }
        return false;
    }

    // Reset the env
    var _dragging        = false;
    var _draggingX       = false;
    var _draggingY       = false;
    var _trottleInput    = 60;
    var _axisX           = $("[data-type='axis-area'][data-axis='x']");
    var _axisY           = $("[data-type='axis-area'][data-axis='y']");
    var _controls        = $("[data-type='controls']");
    var _parentOffsetX   = _axisX.offset();
    var _parentOffsetY   = _axisY.offset();
    var _startX          = Math.round(_axisX.width() / 2);
    var _startY          = Math.round(_axisY.height() / 2);
    var _endX            = _startX;
    var _endY            = _startY;
    var _positionX       = 0;
    var _positionY       = 0;
    var _touchEvents     = ["touchstart", "touchmove", "touchend", "touchcancel"];
    var _mouseEvents     = ["mousedown", "mouseup", "mousemove", "mouseover", "mouseenter", "mouseleave", "mouseout"];
    var _activeKeepAlive = 3;
    var _activeCount     = 0;

    window.setInterval(function(){_mainLoop(); }, _trottleInput);

    var _mainLoop = function() {

        var xPercentile = 0;
        var yPercentile = 0;
        var active      = false;

        if (_draggingY){
            //console.log('STARTY:' + _startY + ', POSY:' + _positionY);
            yPercentile = Math.round((_startY - _positionY) / _startY * 100);
            yPercentile = (yPercentile > 100) ? 100 : yPercentile;
            yPercentile = (yPercentile < -100) ? -100 : yPercentile;
            active      = true;
            _activeCount = 0;
        } else {
            _positionY  = 0;
            yPercentile = 0;
        }

        if (_draggingX){
            //console.log('STARTX:' + _startX + ', POSX:' + _positionX);
            xPercentile = Math.round(- (_startX - _positionX) / _startX * 100);
            xPercentile = (xPercentile > 100) ? 100 : xPercentile;
            xPercentile = (xPercentile < -100) ? -100 : xPercentile;
            active      = true;
            _activeCount = 0;
        } else {
            _positionX  = 0;
            xPercentile = 0;
        }

        // Finally Send the Bluetooth command
        _activeCount++;
        if (active || _activeCount <= (_activeKeepAlive+1)){
            bth.action(
                JSON.stringify({
                    action: "control",
                    x: xPercentile,
                    y: yPercentile
                })
            );
        }

        // Output some data
        $('.axis-output').html("Y:" + yPercentile + ", X:" +xPercentile);
        $('.axis-activity').html("Y:" + +_draggingY + ", X:" + +_draggingX);
    }

    // Create the handlers
    $("[data-type='axis-area']").bind({
        mousedown:      function(event) { _activate(event, $(this)); },
        touchstart:     function(event) { _activate(event, $(this)); },
        mouseup:        function(event) { _complete(event, $(this)); },
        mouseleave:     function(event) { _complete(event, $(this)); },
        touchend:       function(event) { _complete(event, $(this)); },
        touchleave:     function(event) { _complete(event, $(this)); }
    });


    // Let's control the lights somewhat
    $(document).ready(function(){

        // Manually run additional commands
        $(_controls).click(function(event){
            bth.action($(this).data('type'));
        });
    });


    // STEERING EVENT
    $("[data-type='axis-area']").on('touchstart touchmove mouseclick mousemove', _.throttle(
        function(e){
            $.each(e.originalEvent.touches, function(index, value){
                var hitX = $("[data-type='axis-area'][data-axis='x']").hitTest(this.pageX, this.pageY);
                var hitY = $("[data-type='axis-area'][data-axis='y']").hitTest(this.pageX, this.pageY);
                if (hitX) { _positionX = this.pageX - _parentOffsetX.left; }
                if (hitY) { _positionY = this.pageY - _parentOffsetY.top; }
            });
        }, _trottleInput)
    );


    // We need to get starting coords, and set the dragging to enabled
    function _activate(event, $this) {
        event.preventDefault();
        _dragging = true;

        if ($this.data('axis') == "y"){ _draggingY = true; }
        if ($this.data('axis') == "x"){ _draggingX = true; }
    }


    // Once complete, just set the dragging to disabled
    function _complete(event, $this){
        event.preventDefault();
        if (_dragging){ _dragging = false; }
        if ($this.data('axis') == "y" && _draggingY){ _draggingY = false; }
        if ($this.data('axis') == "x" && _draggingX){ _draggingX = false; }
    }

    // Return Nothing
    return {};

})(jQuery);