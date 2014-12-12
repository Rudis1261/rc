var bth = (function($, window, db) {

    var _theLoop;
    var _wasConnected   = false;
    var _connected      = false;
    var _loopInterval   = 1000;
    var _hide           = false;
    var _enabled        = false;
    var _listDevices    = false;
    var _info           = $(".message-centre");
    var _retry          = 0;
    var _maxRetry       = 20;

    /**
     * ON EVENTS (CALLBACK FUNCTIONS)
     */
    function _hideAll() {
        $(".status-on").hide();
        $(".status-off").hide();
        $(".no-devices").hide();
        $(".connected").hide();
        _info.hide();
     }

    function _onEnabled() {
        _hideAll();
        $(".status-on").show();
        $('body').removeClass("off");
        $('body').addClass("on");
        _enabled = true;
        _startConnectionSequence();
    }

    function _error(message) {
        _info.addClass("error").removeClass("info").text(message).show();
    }

    function _message(message) {
        _info.addClass("info").removeClass("remove").text(message).show();
    }

    function _onDisabled() {
        _hideAll();
        $(".status-off").show();
        $('body').addClass("off");
        $('body').removeClass("on");
        _enabled = false;
    }

    function _onNoDevices() {
        _hideAll();
        $(".no-devices").show();
        _connected = false;
    }

    function _setLastConnected() {
        if (db.get("last_device_attempt")) {
            db.set("last_device_success",
                db.get("last_device_attempt")
            );
        }
    }

    function _onConnected(device) {
        console.log("CONNECTED");
        _hideAll();
        _setLastConnected();
        $(".connected").show();
        _listDevices    = false;
        _connected      = true;
        _wasConnected   = true;
        _retry          = 0;
    }

    function _onNotConnected(device) {
        _connected = false;
        console.log("NOT CONNECTED");

        // I swear we were connected, just now!
        if (_wasConnected) {
            _checkReconnect("Connection lost, attempting to reconnect");
        }

        // Should we list the devices?
        if ( ! _listDevices)
        {
            _checkReconnect("Attempting to connect to previous server");
            bluetoothSerial.list(_onDeviceList);
        } else {
            bluetoothSerial.list(_onDeviceList);
        }
    }

    function _connect(device) {
        console.log("CONNETING");
        db.set("last_device_attempt", device);
        bluetoothSerial.connect(device, _onConnected);
    }

    function _reconnect(device) {
        if (_retry <= _maxRetry) {

            _retry += 1;
            _error("Attempting to reconnect (" + _retry + " of " + _maxRetry + ")");
            _connect(device);

        }  else {
            _error("Failed to reconnect!");
        }
    }

    // Attempt to reconnect to the last item
    function _checkReconnect(message) {
        _error(message);
        if (db.get("last_device_success")) {
            _reconnect(db.get("last_device_success"));
        }
    }

    function _startConnectionSequence() {
        bluetoothSerial.isConnected(
            function(){_onConnected();},
            function(){_onNotConnected();}
        );
    }

    function _onDeviceList(devices) {

        // No paired devices
        if (devices.length === 0) {
            _onNoDevices();

        } else {

            $('div.devices').show();
            var deviceList = "";
            devices.forEach(function(device) {
                deviceList += '<li onClick="bth.connect(\'' + device.id + '\');">';
                deviceList += device.name + ' [' + device.id + ']';
                deviceList += '</li>';
            });
            $('ul.devices').html(deviceList);
            _listDevices = true;
        }
    }

    function _construct() {
        $(document).on("deviceready", _init);
        _hideAll();
    }

    function _mainLoop(){
        console.log("SINK INIT");
        _theLoop = setInterval(function(){_loop();}, _loopInterval);
    }

    function _loop() {
        bluetoothSerial.isEnabled(
            _onEnabled,
            _onDisabled
        );
    }

    // Volume Rocker Event Listener
    function _volumeRocker() {
        $(window).on("volumebuttonslistener", function(event){
            if (event.originalEvent.signal){
                if (event.originalEvent.signal == "volume-down"){
                    _action("vol-down");
                }
                if (event.originalEvent.signal == "volume-up"){
                    _action("vol-up");
                }
            }
        });
    }

    // We have a swipe are we need to be able to detect
    function _swipeArea() {
        var actions         = {};
        var actionText      = {};
        actions["right"]    = "prev";
        actions["left"]     = "next";
        actions["up"]       = "play";
        actions["down"]     = "stop";
        actionText["right"] = "Previous";
        actionText["left"]  = "Next";
        actionText["up"]    = "Playing";
        actionText["down"]  = "Stopped";

        $(".swipearea").swipe({
            swipe:function(event, direction, distance, duration, fingerCount){
                if (actions[direction]) {
                    $(this).text(actionText[direction]);
                    bth.action(actions[direction]);
                }
            },
            threshold: $(".swipearea").hasClass('on') ? 80 : 0
        });
    }


    // The skip left and right buttons also need listeners
    function _touchArea() {
        $(".touchable").on("click touchstart", function(){
          console.log("Tap Detected: " + $(this).data("action"));
          bth.action($(this).data("action"));
        });
    }


    // Manage Manual Actions
    function _action(value) {
        bluetoothSerial.write(value, function (data) {
            console.log(data);
        }, function(data){
            console.log(data);
        });
    }

    // Go Button event listener
    function _goButton() {
        $("input[type='text']").on("keydown", function(event){
            if (event.keyCode == 9 || event.keyCode == 13) {
                _action( $(this).val() );
            }
        });
    }

    // Everything has to start somewhere
    function _init() {

        console.log("Bluetooth INIT");

        // Start other listeners as well
        _volumeRocker();
        _goButton();
        _swipeArea();
        _touchArea();
        _loop();
        _mainLoop();
    }

    /**
     * Auto-initilze and construct the module object
     */
    _construct();
    return {
        // Only the connect function is exposed at the moment
        connect: _connect,
        action: _action
    };

})(jQuery, window, db);