
function showpics(id) {
    return new Promise((resolve, reject) => {
        const showdiv = document.getElementById(id);
        const img_dir = '../images';
        fetch('/images')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(files => {
                i = 0;
                for (const file in data) {
                    console.log(file)

                    console.log(data[file])
                    path =encodeURI( '/images/' + file);
                    const newdiv = document.createElement('div');
                    newdiv.className = 'div-of-showpic';
                    newdiv.style.backgroundImage = `url('${path}')`
                    newdiv.dataset.t_100=data[file]["a10"]
                    newdiv.dataset.t_64=data[file]["a6"]
                    showdiv.appendChild(newdiv)
                }
                resolve(files); // 将文件列表传递给下一个 then
            })
            .catch(error => {
                reject(error); // 如果出现错误，将错误信息传递给下一个 catch
            });
    });
}
const id = 'in-time-pic-show';



let data;
let img_path='/images64/';

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


let  big_picture_name

function showpic_all(){
    const showdiv = document.getElementById(id);
    while (showdiv.firstChild) {
        showdiv.removeChild(showdiv.firstChild);
    }
// 调用 showpics 函数并等待其完成
    showpics(id)
        .then(files => {
            // showpics 函数执行完成后执行后续代码
            const divs = document.getElementsByClassName('div-of-showpic');
            const divsArray = Array.prototype.slice.call(divs);
            const main_prview=document.getElementById('picture-show');
            const t_64=document.getElementById('time_64');
            const t_100=document.getElementById('time_100');
            const date=document.getElementById("date");
            

            console.log(data)
            // 为每个 div 元素添加点击事件监听器
            divsArray.forEach(div => {
                div.addEventListener('click', () => {
                    // 获取被点击的 div 的 id
                    const name = div.style.backgroundImage;
                    file_name=name.slice(13,-2);
                    big_picture_name=file_name;
                    file_name= decodeURI(file_name)

                    t_64.textContent=" time_64:  "+data[file_name]["a6"];
                    t_100.textContent="time_100:  "+data[file_name]["a10"];
                    date.textContent="date:  "+data[file_name]["time"];

                    
                    main_prview.style.backgroundImage=`url('${img_path+big_picture_name}')`;
                });
            });
        })
        .catch(error => {
            console.error('Error in showpics:', error);
        });
}

showpic_all()
let maxtime;
let mintime;

// 获取按钮元素
// const popupButton = document.getElementById('shaixuan');
// 获取模态框元素
// const modal = document.getElementById('myModal');
// 获取关闭按钮元素
// const closeButton = document.getElementsByClassName('close')[0];

// const surebutton=document.getElementById('shaixuan-over');

const a_6=document.getElementById('a_6');

const a_10=document.getElementById('a_10');

let flag_64=true;
let flag_100=false;

a_6.addEventListener('click',()=>{
    flag_64=true;
    flag_100=false;
    img_path="/images64/";
    if(big_picture_name !=""){
        const picshow=document.getElementById('picture-show');
        path_64="/images64/"+big_picture_name;
        picshow.style.backgroundImage=`url('${path_64}')`
    }

})
a_10.addEventListener('click',()=>{
    flag_64=false;
    flag_100=true;
    img_path="/images100/"; 
    if(big_picture_name !=""){
        const picshow=document.getElementById('picture-show');
        path_100="/images100/"+big_picture_name;
        picshow.style.backgroundImage=`url('${path_100}')`
    }
})

// // 添加点击事件监听器 显示模态框
// popupButton.addEventListener('click', () => {
//     // 显示模态框
//     modal.style.display = 'block';
// });

// // 添加点击事件监听器，以关闭模态框
// closeButton.addEventListener('click', () => {
//     // 隐藏模态框
//     modal.style.display = 'none';
// });


// 显示筛选过后的结果
// surebutton.addEventListener('click',()=>{
//     const maxtime=document.getElementById("maxtime").value;
//     const mintime=document.getElementById("mintime").value;
//     modal.style.display = 'none';

//     const showdiv = document.getElementById(id);
//     while (showdiv.firstChild) {
//         showdiv.removeChild(showdiv.firstChild);
//     }

//     fetch('/images')
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.json();
//             })
//             .then(files => {
//                 if(flag_100 && flag_64){
//                     console.log("111")
//                     for (const file of files) {
//                         timeof64=data[file]["a6"];
//                         timeof100=data[file]["a10"];
//                         if(timeof64>mintime && timeof64 <maxtime && timeof100>mintime && timeof100 < maxtime){
//                             path = '/images/' + file;
//                             const newdiv = document.createElement('div');
//                             newdiv.className = 'div-of-showpic';
//                             newdiv.style.backgroundImage = `url(${path})`
//                             showdiv.appendChild(newdiv)
//                         }
//                     }
//                 }else if(flag_100 || flag_64){
//                     console.log("222")
//                     for (const file of files) {
                        
//                         timeof64=eval(data[file]["a6"]);
//                         timeof100=eval(data[file]["a10"]);
//                         if(flag_100){
                            
//                             if(timeof100>mintime && timeof100 < maxtime){
//                                 path = '/images/' + file;
//                                 const newdiv = document.createElement('div');
//                                 newdiv.className = 'div-of-showpic';
//                                 newdiv.style.backgroundImage = `url(${path})`
//                                 showdiv.appendChild(newdiv)
//                             }
//                         }else{
//                             console.log("444")
//                             console.log(typeof(timeof64))
                            
//                             if(timeof64>mintime && timeof64 < maxtime){
//                                 path = '/images/' + file;
//                                 const newdiv = document.createElement('div');
//                                 newdiv.className = 'div-of-showpic';
//                                 newdiv.style.backgroundImage = `url(${path})`
//                                 showdiv.appendChild(newdiv)
//                             }
//                         }
//                     }
//                 }else{
//                     console.log("333")
//                     for (const file of files) {
                        
//                         path = '/images/' + file;
//                         const newdiv = document.createElement('div');
//                         newdiv.className = 'div-of-showpic';
//                         newdiv.style.backgroundImage = `url(${path})`
//                         showdiv.appendChild(newdiv)
//                     }
//                 }
                
//             })
//             .then(files => {
//                 // showpics 函数执行完成后执行后续代码
//                 const divs = document.getElementsByClassName('div-of-showpic');
//                 const divsArray = Array.prototype.slice.call(divs);
//                 const main_prview=document.getElementById('picture-show')
//                 const t_64=document.getElementById('time_64')
//                 const t_100=document.getElementById('time_100')
        
        
                
        
//                 console.log(data)
//                 // 为每个 div 元素添加点击事件监听器
//                 divsArray.forEach(div => {
//                     div.addEventListener('click', () => {
//                         // 获取被点击的 div 的 id
//                         const name = div.style.backgroundImage;
//                         // 输出被点击的 div 的 id 到控制台
//                         console.log("Clicked div id:",name );
//                         file_name=name.slice(13,-2);
//                         t_64.textContent=" time_64:  "+data[file_name]["a6"];
//                         t_100.textContent="time_100:  "+data[file_name]["a10"];
//                         console.log(data[file_name]["a6"])
//                         main_prview.style.backgroundImage=name;
//                     });
//                 });
//             })
//             .catch(error => {
//                 console.log(error) // 如果出现错误，将错误信息传递给下一个 catch
//             });

// })

// // 当用户点击模态框外部区域时，关闭模态框
// window.addEventListener('click', (event) => {
//     if (event.target === modal) {
//         modal.style.display = 'none';
//     }
// });


// 定义8*8图块
function get_img64(){
   
    const picshow=document.getElementById('picture-show');
    path_64="/images64/"+big_picture_name;
    picshow.style.backgroundImage=`url('${path_64}')`
    
}

function get_img100(){
   
    
    img_path="/images100/"; 
}

function sure_show(){
    // 显示符合条件的图片
    const maxtime=eval(document.getElementById("maxtime").value);
    const mintime=eval(document.getElementById("mintime").value);
    const showdiv = document.getElementById(id);
    while (showdiv.firstChild) {
        showdiv.removeChild(showdiv.firstChild);
    }
    fetch('/images')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(files => {
                if(flag_100){
                    for (const file of files) {
                        
                    
                        timeof100=eval(data[file]["a10"]);
                        
                    
                        if(timeof100>mintime && timeof100 < maxtime){
                            path = '/images/' + file;
                            const newdiv = document.createElement('div');
                            newdiv.className = 'div-of-showpic';
                            newdiv.style.backgroundImage = `url('${path}')`
                            newdiv.dataset.t_100=data[file]["a10"]
                            newdiv.dataset.t_64=data[file]["a6"]
                            showdiv.appendChild(newdiv)
                        }
                    }
                    
                }else{
                    for (const file of files) {
                        
                        timeof64=eval(data[file]["a6"]);
                        
                       
                        if(timeof64>mintime && timeof64 < maxtime){
                            path = '/images/' + file;
                            const newdiv = document.createElement('div');
                            newdiv.className = 'div-of-showpic';
                            newdiv.style.backgroundImage = `url('${path}')`
                            newdiv.dataset.t_100=data[file]["a10"]
                            newdiv.dataset.t_64=data[file]["a6"]
                            showdiv.appendChild(newdiv)
                        }
                        
                    }
                }

            })
            .then(files => {
                                // showpics 函数执行完成后执行后续代码
                                const divs = document.getElementsByClassName('div-of-showpic');
                                const divsArray = Array.prototype.slice.call(divs);
                                const main_prview=document.getElementById('picture-show')
                                const t_64=document.getElementById('time_64')
                                const t_100=document.getElementById('time_100')
                        
                        
                                
                        
                                console.log(data)
                                // 为每个 div 元素添加点击事件监听器
                                divsArray.forEach(div => {
                                    div.addEventListener('click', () => {
                                        // 获取被点击的 div 的 id
                                        const name = div.style.backgroundImage;
                                        // 输出被点击的 div 的 id 到控制台
                                        console.log("Clicked div id:",name );
                                        file_name=name.slice(13,-2);
                                        big_picture_name=file_name;

                                        file_name= decodeURI(file_name)

                                        t_64.textContent=" time_64:  "+data[file_name]["a6"];
                                        t_100.textContent="time_100:  "+data[file_name]["a10"];
                                        console.log(data[file_name]["a6"])
                                        main_prview.style.backgroundImage=name;
                                    });
                                });
                            });
}

function  creatediv(list){
    const showdiv = document.getElementById(id);
    while (showdiv.firstChild) {
        showdiv.removeChild(showdiv.firstChild);
    }
    const t_64=document.getElementById('time_64')
    const t_100=document.getElementById('time_100')
    const main_prview=document.getElementById('picture-show')
    for (const file of list) {
        const newdiv = document.createElement('div');
        newdiv.className = 'div-of-showpic';
        newdiv.style.backgroundImage = file.style.backgroundImage
        newdiv.dataset.t_100=file.dataset.t_100
        newdiv.dataset.t_64=file.dataset.t_64

        newdiv.addEventListener('click', () => {
            // 获取被点击的 div 的 id
            const name = newdiv.style.backgroundImage;
            // 输出被点击的 div 的 id 到控制台
            console.log("Clicked div id:",name );
            file_name=name.slice(13,-2);
            big_picture_name=file_name;

            file_name= decodeURI(file_name)

            t_64.textContent=" time_64:  "+data[file_name]["a6"];
            t_100.textContent="time_100:  "+data[file_name]["a10"];
            main_prview.style.backgroundImage=`url('${img_path+big_picture_name}')`;
        });

        showdiv.appendChild(newdiv)
    }
}

function upshow(){
    const divs = document.getElementsByClassName('div-of-showpic');
    const divsArray = Array.prototype.slice.call(divs);
    console.log("upshow")
    if(flag_64){
        for(i=1;i<divsArray.length;i++){
            for(j=0;j<divsArray.length-i;j++){
                if(eval(divsArray[j].dataset.t_64)>eval(divsArray[j+1].dataset.t_64)){
                    tempdiv=divsArray[j].style.backgroundImage;
                    divsArray[j].style.backgroundImage=divsArray[j+1].style.backgroundImage;
                    divsArray[j+1].style.backgroundImage=tempdiv;

                    tempdiv=divsArray[j].dataset.t_100;
                    divsArray[j].dataset.t_100=divsArray[j+1].dataset.t_100;
                    divsArray[j+1].dataset.t_100=tempdiv;

                    tempdiv=divsArray[j].dataset.t_64;
                    divsArray[j].dataset.t_64=divsArray[j+1].dataset.t_64;
                    divsArray[j+1].dataset.t_64=tempdiv;
                }
            }
        }
        
    }else{
        for(i=1;i<divsArray.length;i++){
            for(j=0;j<divsArray.length-i;j++){
                if(eval(divsArray[j].dataset.t_100)>eval(divsArray[j+1].dataset.t_100)){
                    tempdiv=divsArray[j].style.backgroundImage;
                    divsArray[j].style.backgroundImage=divsArray[j+1].style.backgroundImage;
                    divsArray[j+1].style.backgroundImage=tempdiv;

                    tempdiv=divsArray[j].dataset.t_100;
                    divsArray[j].dataset.t_100=divsArray[j+1].dataset.t_100;
                    divsArray[j+1].dataset.t_100=tempdiv;

                    tempdiv=divsArray[j].dataset.t_64;
                    divsArray[j].dataset.t_64=divsArray[j+1].dataset.t_64;
                    divsArray[j+1].dataset.t_64=tempdiv;
                }
            }
        }
    }
    console.log(divsArray)
    creatediv(divsArray)
}
function downshow(){
    const divs = document.getElementsByClassName('div-of-showpic');
    const divsArray = Array.prototype.slice.call(divs);
    console.log("downshow")
    if(flag_64){
        for(i=1;i<divsArray.length;i++){
            for(j=0;j<divsArray.length-i;j++){
                if(eval(divsArray[j].dataset.t_64)<eval(divsArray[j+1].dataset.t_64)){
                    tempdiv=divsArray[j].style.backgroundImage;
                    divsArray[j].style.backgroundImage=divsArray[j+1].style.backgroundImage;
                    divsArray[j+1].style.backgroundImage=tempdiv;

                    tempdiv=divsArray[j].dataset.t_100;
                    divsArray[j].dataset.t_100=divsArray[j+1].dataset.t_100;
                    divsArray[j+1].dataset.t_100=tempdiv;

                    tempdiv=divsArray[j].dataset.t_64;
                    divsArray[j].dataset.t_64=divsArray[j+1].dataset.t_64;
                    divsArray[j+1].dataset.t_64=tempdiv;
                }
            }
        }
        
    }else{
        for(i=1;i<divsArray.length;i++){
            for(j=0;j<divsArray.length-i;j++){
                if(eval(divsArray[j].dataset.t_100)<eval(divsArray[j+1].dataset.t_100)){
                    tempdiv=divsArray[j].style.backgroundImage;
                    divsArray[j].style.backgroundImage=divsArray[j+1].style.backgroundImage;
                    divsArray[j+1].style.backgroundImage=tempdiv;

                    tempdiv=divsArray[j].dataset.t_100;
                    divsArray[j].dataset.t_100=divsArray[j+1].dataset.t_100;
                    divsArray[j+1].dataset.t_100=tempdiv;

                    tempdiv=divsArray[j].dataset.t_64;
                    divsArray[j].dataset.t_64=divsArray[j+1].dataset.t_64;
                    divsArray[j+1].dataset.t_64=tempdiv;
                }
            }
        }
    }
    console.log(divsArray)
    creatediv(divsArray)
}



//搜索功能，鼠标点击之后库中只有目标图片

function search_click(){
    const search_text=document.getElementById('search-text');
    intext=search_text.value;
    var result_list=[];
    const showdiv = document.getElementById(id);
    const t_64=document.getElementById('time_64');
    const t_100=document.getElementById('time_100');
    const main_prview=document.getElementById('picture-show');
    const date=document.getElementById("date");

    while (showdiv.firstChild) {
        showdiv.removeChild(showdiv.firstChild);
    }
    for(key in data){
        
        if( key.includes(intext)){
            result_list.push(key);
        }

    }


    result_list.forEach(file=>{
        console.log(file)

        console.log(data[file])
        path =encodeURI( '/images/' + file);
        const newdiv = document.createElement('div');
        newdiv.className = 'div-of-showpic';
        newdiv.style.backgroundImage = `url('${path}')`
        newdiv.dataset.t_100=data[file]["a10"]
        newdiv.dataset.t_64=data[file]["a6"]

        newdiv.addEventListener('click', () => {
            // 获取被点击的 div 的 id
            const name = newdiv.style.backgroundImage;
            // 输出被点击的 div 的 id 到控制台
            console.log("Clicked div id:",name );
            file_name=name.slice(13,-2);
            big_picture_name=file_name;

            file_name= decodeURI(file_name)
            console.log(file_name)

            t_64.textContent=" time_64:  "+data[file_name]["a6"];
            t_100.textContent="time_100:  "+data[file_name]["a10"];
            main_prview.style.backgroundImage=`url('${img_path+big_picture_name}')`;
            date.textContent="date:  "+data[file_name]["time"];
        });

        showdiv.appendChild(newdiv)
    });
        
    
}