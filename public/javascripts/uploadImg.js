id='showarea';
showpics(id)

// 上传图片
function uploadimg() {
  const fileInput = document.getElementById('imageInput');
  const files = fileInput.files; // 获取用户选择的文件列表
  const formdata = new FormData();

  // 遍历文件列表，将每个文件添加到 FormData 中
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    console.log(file.type);
    console.log(file.name);
    formdata.append('files[]', file); // 注意这里使用 files[] 来表示多个文件
  }

  fetch('http://localhost:9000/save_img', {
      method: 'POST', // 使用POST方法
      mode:'cors',
      body:  formdata
      })
      .then(response => response.json())
      .then(data => {
        inputImg.style.backgroundImage=`url('${encodeURI(data['message'][0])}')`
        showpics(id)
      })
      .catch(error => console.error('Error:', error));

  showpics(id)
}


//如果是直接拖入的话
const inputImg=document.getElementById('preview');

inputImg.addEventListener('dragover', (e) => {
  e.preventDefault();
  inputImg.classList.add('highlight');
});

inputImg.addEventListener('dragleave', () => {
  inputImg.classList.remove('highlight');
});

inputImg.addEventListener('drop', (e) => {
  e.preventDefault();
  inputImg.classList.remove('highlight');
  const files = e.dataTransfer.files;
  handleFiles(files);
});


// 拖曳输入图片，输入的顺序不确定
function handleFiles(files) {

  const formdata = new FormData();
  // console.log(files)
  for (const file of files) {
    formdata.append('files[]', file);
    // 这里可以将文件上传到服务器
  }
  fetch('http://localhost:9000/save_img', {
      method: 'POST', // 使用POST方法
      mode:'cors',
      body:  formdata
      })
      .then(response => response.json())
      .then(data => {
        inputImg.style.backgroundImage=`url('${data['message'][0]}')`
        showpics(id)
      })
      .catch(error => console.error('Error:', error));

  showpics(id)
}


