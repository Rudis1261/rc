(function($){

    // Reset the env
    var _dragging      = false;
    var _trottleInput  = 10;
    var _axisX         = $("[data-type='drag-area'][data-axis='x']");
    var _axisY         = $("[data-type='drag-area'][data-axis='y']");
    var _parentOffsetX = _axisX.offset();
    var _parentOffsetY = _axisY.offset();
    var _startX        = Math.round(_axisX.width() / 2);
    var _startY        = Math.round(_axisY.height() / 2);
    var _endX          = _startX;
    var _endY          = _startY;

    window.setInterval(function(){_zero();}, 200);

    var _zero = function() {
        //console.log("TESTING");
        if (_dragging == false && (_endX != 0 || _endY != 0)) {
            _endY = 0;
            _endX = 0;
            console.log("ZEROING");
        }

        else if (_dragging) {

        }
    }

    // Get the coords regardless whether it's a mouse or touch event
    var pointerPositionXY = function(e){
        var out = {x:0, y:0};
        var touchEvents = ["touchstart", "touchmove", "touchend", "touchcancel"];
        var mouseEvents = ["mousedown", "mouseup", "mousemove", "mouseover", "mouseenter", "mouseleave", "mouseout"];

        if (touchEvents.indexOf(e.type)){
            // Touch Type events
            var touch = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
            out.x = touch.pageX - _parentOffsetX.left;
            out.y = touch.pageY - _parentOffsetY.top;

        } else if (mouseEvents.indexOf(e.type)){
            // Mouse Type events
            out.x = e.pageX - _parentOffsetX.left;
            out.y = e.pageY - _parentOffsetY.top;
        }
        return out;
    };

    // Create the handlers
    $("[data-type='drag-area']").bind({
        mousedown:      function(event) { _activate(event); },
        touchstart:     function(event) { _activate(event); },
        mouseup:        function(event) { _complete(event); },
        mouseleave:     function(event) { _complete(event); },
        touchend:       function(event) { _complete(event); },
        touchleave:     function(event) { _complete(event); }
    });

    // Throttle the mouse moves somewhat, to ensure we do not flood the comms
    $("[data-type='drag-area']").on('touchmove mousemove', _.throttle(
        function(event){
            _track(event, $(this));
        },_trottleInput)
    );

    // We need to get starting coords, and set the dragging to enabled
    function _activate(event) {
        event.preventDefault();
        var getXY   = pointerPositionXY(event);
        _dragging   = true;
    }

    // On mouse move / touch move, this tracks the position and sends the commands
    function _track(event, element) {
        event.preventDefault();
        if (_dragging) {

            // Get the current position, and the distance we have since dragged
            var getXY = pointerPositionXY(event);

            if (element.data('axis') == 'x') {
                _endX = getXY.x;
            }

            if (element.data('axis') == 'y') {
                _endY = getXY.y;
            }

            _getDistance = _distance();
            var xPercentile = Math.round(_getDistance.x / _startX * 100);
            var yPercentile = Math.round(- _getDistance.y / _startY * 100);

            xPercentile = (xPercentile > 100) ? 100 : xPercentile;
            xPercentile = (xPercentile < -100) ? -100 : xPercentile;

            yPercentile = (yPercentile > 100) ? 100 : yPercentile;
            yPercentile = (yPercentile < -100) ? -100 : yPercentile;
            console.log("DIST_Y: " + yPercentile + ", DIST_X: " + xPercentile);

            $('.output').html("Y:" + yPercentile + ", X:" + xPercentile);

            console.log(JSON.stringify({
                action: "control",
                x: xPercentile,
                y: yPercentile
            }));


            // Send the command via the BTH
            /*bth.action(
                JSON.stringify({
                    action: "mouse-move",
                    x: _getDistance.x,
                    y: _getDistance.y
                })
            );*/
            //_.throttle(_track(event, element),_trottleInput);
        }
    }

    // Once complete, just set the dragging to disabled
    function _complete(event){
        event.preventDefault();
        if (_dragging) {
            _dragging = false;
        }
    }

    // We need to be able to determine how far the dragging action was
    function _distance() {
        var out = { x:0, y:0 };
        if ( _dragging) {
            out.x = _endX - _startX;
            out.y = _endY - _startY;
        }
        return out;
    }

    // Return Nothing
    return {};

})(jQuery);