const gulp = require('gulp');
const uglify = require('gulp-uglify');
const pump = require('pump');
const version = require('gulp-version-number');
const autoprefixer = require('gulp-autoprefixer');
const sourcemaps=require('gulp-sourcemaps');
const runSequence = require('run-sequence');
const del = require('del');
const cssmin = require('gulp-minify-css');
const imagemin = require('gulp-imagemin');
const clean = require('gulp-clean');
//const flatten = require('gulp-flatten');
const pngquant = require('imagemin-pngquant');
//const cache = require('gulp-cache');

const DEST_DIR='app/';
const SRC_DIR='websrc/';
const TEMP_DIR_NAME='templates';
const STATIC_DIR_NAME='static';
// Environment setup.
var env = {
    production: false
};

// Environment task.
gulp.task("set-production", function(){
    env.production = true;
});

const versionConfig = {
  'value': '%MDS%',
  'append': {
    'key': 'v',
    'to': ['css', 'js','image'],
  },
};

gulp.task('html',()=>{
	return gulp.src(SRC_DIR+TEMP_DIR_NAME+'/**/*.html')
    .pipe(version(versionConfig))
    .pipe(gulp.dest(DEST_DIR+TEMP_DIR_NAME));
});
gulp.task('jsmin', function (cb) {
	if(env.production){
		return gulp.src([SRC_DIR+STATIC_DIR_NAME+'/**/*.js'])
        .pipe(uglify({mangle: {except: ['require' ,'exports' ,'module' ,'$']}})) //排除混淆关键字
        .pipe(gulp.dest(DEST_DIR+STATIC_DIR_NAME));
	}
	else{
		return gulp.src([SRC_DIR+STATIC_DIR_NAME+'/**/*.js'])
		//.pipe(sourcemaps.init())
       // .pipe(uglify({mangle: {except: ['require' ,'exports' ,'module' ,'$']}})) //排除混淆关键字
	//	.pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(DEST_DIR+STATIC_DIR_NAME));
	}
	
});
gulp.task('cssmin', function () {
	if(env.production){
		return gulp.src(SRC_DIR+STATIC_DIR_NAME+'/**/*.css')
		//.pipe(concat('main.css'))
        .pipe(autoprefixer('last 2 version', 'safari 5', 'ie 8', 'ie 9', 'opera 12.1', 'ios 6', 'android 4'))
        .pipe(cssmin())
        .pipe(gulp.dest(DEST_DIR+STATIC_DIR_NAME));
	}
	else{
		return gulp.src(SRC_DIR+STATIC_DIR_NAME+'/**/*.css')
		//.pipe(concat('main.css'))
        .pipe(autoprefixer('last 2 version', 'safari 5', 'ie 8', 'ie 9', 'opera 12.1', 'ios 6', 'android 4'))
		//.pipe(sourcemaps.init())
		
        //.pipe(cssmin())
		//.pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(DEST_DIR+STATIC_DIR_NAME));
	}
    
});
gulp.task('rawtoone', () =>{
    return gulp.src([SRC_DIR+STATIC_DIR_NAME+'/**/*.{png,jpg,jpeg,gif,bmp,ico}',SRC_DIR+'/**/*.{swf,eot,svg,ttf,woff}'])
        .pipe(flatten())
		//.pipe(imagemin())
        .pipe(gulp.dest(DEST_DIR+STATIC_DIR_NAME));
	}
);
gulp.task('dokuimgmin', () =>{
    return gulp.src(['data/dokuwiki'+'/**/*.{png,jpg,jpeg,gif,bmp,ico}'])
		.pipe(
			//cache(
			imagemin({
			optimizationLevel: 5, //类型：Number  默认：3  取值范围：0-7（优化等级）
            progressive: true, //类型：Boolean 默认：false 无损压缩jpg图片
            interlaced: true, //类型：Boolean 默认：false 隔行扫描gif进行渲染
            multipass: true, //类型：Boolean 默认：false 多次优化svg直到完全优化
			svgoPlugins: [{removeViewBox: false}],//不要移除svg的viewbox属性
			use: [pngquant()] //使用pngquant深度压缩png图片的imagemin插件
		})
		//)
		)
        .pipe(gulp.dest('data/dokuwiki2'));
	}
);
gulp.task('copy', () =>{
    return gulp.src([SRC_DIR+STATIC_DIR_NAME+'/**/*.{png,jpg,jpeg,gif,bmp,ico}',SRC_DIR+STATIC_DIR_NAME+'/**/*.{swf,eot,svg,ttf,woff}'])
        .pipe(gulp.dest(DEST_DIR+STATIC_DIR_NAME));
	}
);
// Clean
gulp.task('clean', function(cb) {
   return  del([DEST_DIR+STATIC_DIR_NAME,DEST_DIR+TEMP_DIR_NAME],cb);
      // return gulp.src('build', {read: false,force: true})
      //  .pipe(clean());
});
// Default task
gulp.task('dev',function(callback) {
    runSequence('clean',['html', 'jsmin','cssmin','copy'],callback);
});

gulp.task('product',function(callback) {
    runSequence('set-production','clean',['html', 'jsmin','cssmin','copy'],callback);
});
gulp.task('watch', function() {
  gulp.watch(SRC_DIR+TEMP_DIR_NAME+'/**/*.html',['html']);
  // Watch .js files
  gulp.watch(SRC_DIR+STATIC_DIR_NAME+'/**/*.js', ['jsmin']);
  // Watch image files
  gulp.watch(SRC_DIR+STATIC_DIR_NAME+'/**/*.css', ['cssmin']);
  gulp.watch([SRC_DIR+STATIC_DIR_NAME+'/**/*.{png,jpg,jpeg,gif,bmp,ico}',SRC_DIR+STATIC_DIR_NAME+'/**/*.{swf,eot,svg,ttf,woff}'],['copy']);
  // Create LiveReload server
  //livereload.listen();
  // Watch any files in dist/, reload on change
  //gulp.watch(['dist/**']).on('change', livereload.changed);
});