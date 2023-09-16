import { dragdrop } from './imagehelper.js'

$(function () {
  dragdrop();

  function preparedata (file) {
    console.log("Preparing ...")
    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
      let fd = new FormData();
      fd.append('file', file);
      console.log("fd: ", fd);
      uploadData(fd);
  }

  // Drop
  $('.upload-area').on('drop', function (e) {
    e.stopPropagation();
    e.preventDefault();
    $("#howto").text("We are uploading your file.");
    let file = e.originalEvent.dataTransfer.files;
    console.log("File uploaded: ", file);
    preparedata(file[0]);
    console.log("done drop.")
  });

  // Open file selector on div click
  $("#uploadfile").click(function () {
    $("#file").click();
  });

  // file selected
  $("#file").change(function () {
    let file = $('#file')[0].files[0];
    console.log("file.size: ", file.size);
    $("#howto").text("Uploading your file.");
    console.log("file: ", file);
    preparedata(file);
  });
});


// Sending AJAX request and upload file
function uploadData (formdata) {

  $.ajax({
    url: '/new/',
    type: 'post',
    data: formdata,
    contentType: false,
    processData: false,
    success: function (data) {
      updatetags(data);
    }
  });
}

function updatetags (data) {
  let original = `<p>"/${data.thumb_path}" </p>`;
  $("#original").html(original);

  $("#howto").html("Drag and Drop file here<br />Or<br />Click to Upload")
}

