(function($){

    // Reset the env
    var _startX         = 0;
    var _startY         = 0;
    var _endX           = 0;
    var _endY           = 0;
    var _dragging       = false;
    var _trottleInput   = 20;

    // Get the coords regardless whether it's a mouse or touch event
    var pointerPositionXY = function(e){
        var out = {x:0, y:0};
        var touchEvents = ["touchstart", "touchmove", "touchend", "touchcancel"];
        var mouseEvents = ["mousedown", "mouseup", "mousemove", "mouseover", "mouseenter", "mouseleave", "mouseout"];

        if (touchEvents.indexOf(e.type)){
            // Touch Type events
            var touch = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
            out.x = touch.pageX;
            out.y = touch.pageY;

        } else if (mouseEvents.indexOf(e.type)){
            // Mouse Type events
            out.x = e.pageX;
            out.y = e.pageY;
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
            _track(event);
        },_trottleInput)
    );

    // We need to get starting coords, and set the dragging to enabled
    function _activate(event) {
        event.preventDefault();
        var getXY   = pointerPositionXY(event);
        _dragging   = true;
        _startX     = getXY.x;
        _startY     = getXY.y;
    }

    // On mouse move / touch move, this tracks the position and sends the commands
    function _track(event) {
        event.preventDefault();
        if (_dragging) {

            // Get the current position, and the distance we have since dragged
            var getXY       = pointerPositionXY(event);
            _endX           = getXY.x;
            _endY           = getXY.y;
            _getDistance    = _distance();

            // Send the command via the BTH
            bth.action(
                JSON.stringify({
                    action: "mouse-move",
                    x: _getDistance.x,
                    y: _getDistance.y
                })
            );

            // Set the start to the current positions. This ensures that movements are relative
            _startX = _endX;
            _startY = _endY;
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