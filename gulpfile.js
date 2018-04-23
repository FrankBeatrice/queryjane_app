var gulp         = require('gulp');
var browserSync  = require('browser-sync');
var autoprefixer = require('autoprefixer');
var postcss      = require('gulp-postcss');
var sass         = require('gulp-sass');
var sourcemaps   = require('gulp-sourcemaps');
var browserify   = require('browserify');
var gutil        = require('gulp-util');
var tap          = require('gulp-tap');
var buffer       = require('gulp-buffer');
var uglify       = require('gulp-uglify');
var rename       = require('gulp-rename');
var babelify     = require('babelify');

var conf = {
  cssAssets: {
    src: [
      './node_modules/bootstrap/dist/css/bootstrap.min.css',
      './node_modules/bootstrap/dist/css/bootstrap.min.css.map',
      './node_modules/jquery-confirm/dist/jquery-confirm.min.css'
    ],
    dest: './app/static/dist/assets/css/'
  },
  jsAssets: {
    src: [
      './node_modules/jquery/dist/jquery.min.js',
      './node_modules/bootstrap/dist/js/bootstrap.min.js',
      './node_modules/jquery-validation/dist/jquery.validate.js',
      './node_modules/jquery-validation/dist/additional-methods.js',
      './node_modules/jquery-confirm/dist/jquery-confirm.min.js',
      './node_modules/typeahead.js/dist/typeahead.bundle.min.js'
    ],
    dest: './app/static/dist/assets/js/'
  }
}

// CSS assets
gulp.task('css-assets', function() {
  return gulp.src(conf.cssAssets.src)
    .pipe(gulp.dest(conf.cssAssets.dest));
});

// Js assets
gulp.task('js-assets', function() {
  return gulp.src(conf.jsAssets.src)
    .pipe(gulp.dest(conf.jsAssets.dest));
});

// SASS
gulp.task('compile-sass', function() {
  return gulp.src('./app/static/sass/**/*.scss')
    .pipe(sourcemaps.init())
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(postcss([ autoprefixer() ]))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('./app/static/dist/css/'))
    .pipe(browserSync.stream());
});

// JS´s
gulp.task('js', function () {
  return gulp.src(
    './app/static/js/**/*.js',
    {read: false}) // No need of reading file because browserify does.
    // Transform file objects using gulp-tap plugin
    .pipe(tap(function (file) {
      gutil.log('bundling ' + file.path);
      // Replace file contents with browserify's bundle stream
      file.contents =
        browserify(file.path, {debug: true})
        .transform('babelify', {presets: ['env', 'es2015']})
        .bundle();
    }))
    // Transform streaming contents into buffer contents (because gulp-sourcemaps does not support streaming contents)
    .pipe(buffer())
    // Load and init sourcemaps
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(uglify())
    .pipe(rename({suffix: '.min'}))
    // Write sourcemaps
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./app/static/dist/js/'));
});

// Images
gulp.task('images', function() {
  return gulp.src('./app/static/img/**/*')
    .pipe(gulp.dest('./app/static/dist/img/'));
});

gulp.task('watch', function() {
  browserSync.init({
    notify: false,
    proxy: 'localhost:8000'
  });

  gulp.watch('./app/static/img/**/*', ['images']);
  gulp.watch('./app/static/sass/**/*.scss', ['compile-sass', browserSync.reload]);
  gulp.watch('./app/static/js/**/*.js', ['js', browserSync.reload]);
  gulp.watch('{app,userprofile}/templates/**/*.html', browserSync.reload);
});

gulp.task('default', ['css-assets', 'js-assets', 'compile-sass', 'js', 'images']);
