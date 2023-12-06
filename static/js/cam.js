(function() {
    // The width and height of the captured photo. We will set the
    // width to the value defined here, but the height will be
    // calculated based on the aspect ratio of the input stream.

    var width = 320; // We will scale the photo width to this
    var height = 0; // This will be computed based on the input stream

    // |streaming| indicates whether or not we're currently streaming
    // video from the camera. Obviously, we start at false.

    var streaming = false;
    let csr = $("input[name=csrfmiddlewaretoken").val();
    glob = {
        d: d1,
        csrfmiddlewaretoken: csr,
    };

    // The various HTML elements we need to configure or control. These
    // will be set by the startup() function.

    var video = null;
    var canvas = null;
    var photo = null;
    var startbutton = null;
    var interval = null;
    var cand_id = null;
    var application_id = null;
    var time_in_secs = null;

    function startup() {
        video = document.getElementById("video");
        canvas = document.getElementById("canvas");
        // photo = document.getElementById("photo");
        webimg = document.getElementById("webimg");
        // startbutton = document.getElementById("startbutton");
        cand_id = document.getElementById("cand_id").value;
        application_id = document.getElementById("application_id").value;

        console.log(cand_id, application_id)

        time_in_secs = document.getElementById("time_in_secs").value;
        console.log(cand_id, time_in_secs);

        navigator.mediaDevices
            .getUserMedia({ video: true, audio: false })
            .then(function(stream) {
                video.srcObject = stream;
                video.play();
            })
            .catch(function(err) {
                console.log("An error occurred: " + err);
            });

        video.addEventListener(
            "canplay",
            function(ev) {
                if (!streaming) {
                    height = video.videoHeight / (video.videoWidth / width);

                    // Firefox currently has a bug where the height can't be read from
                    // the video, so we will make assumptions if this happens.

                    if (isNaN(height)) {
                        height = width / (4 / 3);
                    }

                    video.setAttribute("width", width);
                    video.setAttribute("height", height);
                    canvas.setAttribute("width", width);
                    canvas.setAttribute("height", height);
                    streaming = true;

                    // Start capturing images automatically every 2 minutes
                    console.log("1st Camshot!");
                    takepicture();
                    interval_time = time_in_secs / 3;
                    console.log("Interval time: " + interval_time);
                    interval = setInterval(function() {
                        console.log("time for SS");
                        takepicture();
                    }, interval_time * 1000);
                }
            },
            false
        );
        // clearphoto();
    }

    // Fill the photo with an indication that none has been
    // captured.

    function clearphoto() {
        var context = canvas.getContext("2d");
        context.fillStyle = "#AAA";
        context.fillRect(0, 0, canvas.width, canvas.height);

        var data = canvas.toDataURL("image/png");
        // photo.setAttribute("src", data);
        webimg.setAttribute("value", data);
    }

    // Capture a photo by fetching the current contents of the video
    // and drawing it into a canvas, then converting that to a PNG
    // format data URL. By drawing it on an offscreen canvas and then
    // drawing that to the screen, we can change its size and/or apply
    // other changes before drawing it.
    var count = 0;

    function takepicture() {
        application_id = document.getElementById("application_id").value;

        console.log("takepicture called =", application_id)
        if (count === 4) {
            clearInterval(interval)
        } else {
            console.log(count)
            var context = canvas.getContext("2d");
            if (width && height) {
                canvas.width = width;
                canvas.height = height;
                context.drawImage(video, 0, 0, width, height);

                var data = canvas.toDataURL("image/png");
                // photo.setAttribute("src", data);
                webimg.setAttribute("value", data);
                console.log("1")
                var form = document.getElementById("inputForm");
                var formData = new FormData(form);
                formData.append(
                    "csrfmiddlewaretoken",
                    $("input[name=csrfmiddlewaretoken").val()
                );
                console.log("out of ajax: ", formData)

                let url = '/camshot_picture/' + application_id;
                $.ajax({
                    url: url,
                    method: "POST",
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function(data) {
                        console.log(data);
                        console.log("success")
                        count++;
                    },
                    error: function(data) {
                        console.error(data);
                        console.log("error")
                        count++;
                    }
                });
                // var xhr = new XMLHttpRequest();
                // xhr.open("POST", window.location.href);
                // xhr.onreadystatechange = function () {
                //   if (xhr.readyState === 4 && xhr.status === 200) {
                //     // Handle the successful response here
                //     console.log(xhr.responseText);
                //   }
                // };
                // xhr.send(formData);

            } else {
                clearphoto();
            }
        }
    }
    // Set up our event listener to run the startup process
    // once loading is complete.
    window.addEventListener("load", startup, false);
})();