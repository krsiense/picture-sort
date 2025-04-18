function showpics(id){
  
      const showdiv=document.getElementById(id);
      const img_dir='../images'
      
      fetch('/images')
      .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(files => {
          i=0;
          while(showdiv.firstChild){
            showdiv.removeChild(showdiv.firstChild);
          }
          for (const file in data) {
              path='/images/'+file;
              const newdiv=document.createElement('div');
              newdiv.className='div-of-showpic';
              console.log(path)
              newdiv.style.backgroundImage=`url('${path}')` 
              showdiv.appendChild(newdiv)
              
            }

            const divs = document.getElementsByClassName('div-of-showpic');
          
          // 在这里处理获取到的文件列表
        })
        .catch(error => {
          console.error('Error fetching files:', error);
        });
      
}
let data=[];
fetch('/data/data.json')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(jsonData => {
    // 在请求成功后将数据赋值给外部定义的变量
    data = jsonData;
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });

// const divider = document.getElementById('divider');
// let isDragging = false;

// divider.addEventListener('mousedown', (e) => {
//     isDragging = true;
// });

// document.addEventListener('mousemove', (e) => {
//     if (!isDragging) return;
    
//     const mouseY = e.clientY;
//     const windowHeight = window.innerHeight;
//     const topDivHeight = mouseY / windowHeight * 100; // 上方div的高度占比
    
//     const top=document.getElementById('top');
//     // 设置上方div和下方div的高度占比
//     top.style.height = `${topDivHeight}%`;
//     document.getElementsByClassName('main-button-div').style.height = `${100 - topDivHeight}%`;
// });

// document.addEventListener('mouseup', () => {
//     isDragging = false;
// });





