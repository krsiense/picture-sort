const { error } = require('console');
var express = require('express');
var router = express.Router();
const path = require('path');
const fs=require('fs')


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/index',function(req,res,next){
  res.sendFile(path.join(__dirname, '../views/index.html'));
})

router.get('/test',function(req,res,next){
  res.sendFile(path.join(__dirname, '../views/test.html'));
})

router.get('/attribute',function(req,res,next){
  res.sendFile(path.join(__dirname, '../views/attribute.html'));
})

router.get('/time',function(req,res,next){
  res.sendFile(path.join(__dirname, '../views/time.html'));
})

router.get('/colorpick',function(req,res,next){
  res.sendFile(path.join(__dirname, '../views/colorpick.html'));
})

router.get('/picdata',function(req,res,next){
  res.sendFile(path.join(__dirname, '../views/picdata.html'));
})

router.get('/images', (req, res) => {
  const directoryPath = path.join(__dirname,'../public','/images'); // 指定图片文件夹路径
  const files = fs.readdirSync(directoryPath); // 读取文件夹下的文件列表
  res.json(files); // 返回文件列表
  
});



module.exports = router;
