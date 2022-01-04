// 이미지 업로드스크립트
function DropFile(dropAreaId, fileListId) {
  let dropArea = document.getElementById(dropAreaId);
  let fileList = document.getElementById(fileListId);

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function highlight(e) {
    preventDefaults(e);
    dropArea.classList.add("highlight");
  }

  function unhighlight(e) {
    preventDefaults(e);
    dropArea.classList.remove("highlight");
  }

  function handleDrop(e) {
    unhighlight(e);
    let dt = e.dataTransfer;
    let files = dt.files;

    handleFiles(files);

    const fileList = document.getElementById(fileListId);
    if (fileList) {
      fileList.scrollTo({ top: fileList.scrollHeight });
    }
  }

  function handleFiles(files) {
    files = [...files];
    files.forEach(previewFile);
  }

  function previewFile(file) {
    console.log(file);
    renderFile(file);
  }

  function renderFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function () {
      let img = dropArea.getElementsByClassName("preview")[0];
      img.src = reader.result;
      img.style.display = "block";
      console.log(img);
    };
  }

  dropArea.addEventListener("dragenter", highlight, false);
  dropArea.addEventListener("dragover", highlight, false);
  dropArea.addEventListener("dragleave", unhighlight, false);
  dropArea.addEventListener("drop", handleDrop, false);

  return {
    handleFiles
  };
}

const dropFile = new DropFile("drop-file", "files");
var preview_img = document.querySelector('#feed_image_file');

//업로드 버튼 누를때 파일 전송하는 함수
function posting() {
  let comment = $('#feed_content').val()
  let file = $('#chooseFile')[0].files[0]
  let form_data = new FormData()
  console.log(file);

  form_data.append("comment_give", comment)
  form_data.append("filename_give", file)

  if (!file) {
    alert('이미지를 업로드해 주세요.');
    return;
  }

  $.ajax({
        type: "POST",
        url: "/upload_page",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response["msg"])
            window.location.href = "/main_page"
        }
    });


}
function to_main() {
    location.href = "/main_page"
}

function to_search() {
    location.href = '/search'
}

function to_upload() {
    location.href = '/write'
}

function to_favorite() {
    location.href = "../../favorite_page/templates/favorite_page.html"
}

function to_mypage() {
    location.href = "/my_page"
}

function to_user_pg() {
    location.href = '../../other_user_page/templates/other_user_page.html'
}
function go_back() {
    window.history.back();
}
