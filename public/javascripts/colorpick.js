

document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggleButton');
    const leftTools = document.getElementById('tools');
    const picbody=document.getElementById('pic-body');

    // 添加点击事件监听器
    toggleButton.addEventListener('click', function() {
        leftTools.classList.toggle('tools-show'); // 切换 show 类
        picbody.classList.toggle('pic-body-show')
    });
});



// 模态框js
  // 打开模态框函数
  function openModal() {
    var modalOverlay = document.getElementById('modalOverlay');
    modalOverlay.style.display = 'block'; // 显示遮罩层
    console.log(222)
}

// 关闭模态框函数
function closeModal() {
    var modalOverlay = document.getElementById('modalOverlay');
    modalOverlay.style.display = 'none'; // 隐藏遮罩层
    const rgb_div=document.getElementById('color-show-rgb');
    const pic_div=document.getElementById('picture-show');

    temp_text=rgb_div.textContent;
    pic_div.style.backgroundColor=temp_text
    temp_text=temp_text.slice(4,-1);
    temp=temp_text.split(',');
    c1=temp[0];
    c2=temp[1].slice(1);
    c3=temp[2].slice(1);
    getcolor(c1,c2,c3)
}


// 获取模态框和模态框边框元素
var modal = document.getElementById('modal');
var modalBorder = document.getElementById('modal-border');

// 定义变量来存储鼠标位置
var offsetX, offsetY;
console.log(modalBorder)
// 鼠标按下事件
modalBorder.onmousedown = function(e) {
    console.log(333);
  // 计算鼠标位置相对于模态框左上角的偏移量
  offsetX = e.clientX - modal.offsetLeft;
  offsetY = e.clientY - modal.offsetTop;

  // 当鼠标移动时，调用 onMouseMove 函数
  document.onmousemove = onMouseMove;
};

// 鼠标移动事件
function onMouseMove(e) {
  // 计算模态框新的位置
  var left = e.clientX - offsetX;
  var top = e.clientY - offsetY;

  // 设置模态框的新位置
  modal.style.left = left + 'px';
  modal.style.top = top + 'px';
}

// 鼠标松开事件
document.onmouseup = function() {
  // 清除鼠标移动事件监听器
  document.onmousemove = null;
};




const picshow=document.getElementById("in-color-pic-show");

let jsdata;

fetch('/data/data.json')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(jsonData => {
    // 在请求成功后将数据赋值给外部定义的变量
    jsdata = jsonData;
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });


  fetch('/images')
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
  })
  .then(files => {
      i = 0;
      for (const file in jsdata) {
        
        path =encodeURI( '/images/' + file);
        const outdiv=document.createElement('div');
        outdiv.className="o-div";
        const label1=document.createElement('label')
        const label2=document.createElement('label')
        const label3=document.createElement('label')
        const newdiv = document.createElement('div');
        newdiv.className = 'div-of-showpic';
        newdiv.style.backgroundImage = `url('${path}')`
        newdiv.dataset.t_100=jsdata[file]["a10"]
        newdiv.dataset.t_64=jsdata[file]["a6"]
        label1.textContent="64: "+jsdata[file]["a6"];
        label2.textContent="100: "+jsdata[file]["a10"];
        outdiv.appendChild(newdiv)
        outdiv.appendChild(label1)
        outdiv.appendChild(label2)
        picshow.appendChild(outdiv)
      }
  
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });


let path

function getcolor(n1,n2,n3){

  str=n1+','+n2+','+n3;
  console.log(str);
  fetch('http://localhost:9000/get_color',{
      method: 'POST', // 使用POST方法
      mode:'cors',
      body:  str
  })
  .then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data=>{
    console.log(data.message)
    const showdiv=document.getElementById('in-color-pic-show')

    while (showdiv.firstChild) {
      showdiv.removeChild(showdiv.firstChild);
  }

    mytest(str)
  })
  
}
let da;

function mytest(str){
  fetch(`/results/${str}/output_json.json`)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(jsonData => {
    const showdiv=document.getElementById('in-color-pic-show')
    while (showdiv.firstChild) {
      showdiv.removeChild(showdiv.firstChild);
    }
    // 在请求成功后将数据赋值给外部定义的变量
    da=jsonData;
    for(key in da){
      filename=key+".jpg";
      path =encodeURI( '/images/' + filename);
      const outdiv=document.createElement('div');
      outdiv.className="o-div";
      const label1=document.createElement('label')
      const label2=document.createElement('label')
      const label3=document.createElement('label')
      const newdiv = document.createElement('div');
      newdiv.className = 'div-of-showpic';
      newdiv.style.backgroundImage = `url('${path}')`
      newdiv.dataset.t_100=jsdata[filename]["a10"]
      newdiv.dataset.t_64=jsdata[filename]["a6"]
      label1.textContent="64: "+jsdata[filename]["a6"];
      label2.textContent="100: "+jsdata[filename]["a10"];
      outdiv.appendChild(newdiv)
      outdiv.appendChild(label1)
      outdiv.appendChild(label2)
      picshow.appendChild(outdiv)
    }
    
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });
}