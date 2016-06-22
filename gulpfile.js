var browserSync = require('browser-sync');
var gulp = require('gulp');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');

gulp.task('compile-sass', function() {
    gulp.src('app/static/sass/*.sass')
        .pipe(sourcemaps.init())
        .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('app/static/css/'))
        .pipe(browserSync.stream());
});

gulp.task('watch', function() {
    browserSync.init({
        notify: false,
        proxy: 'localhost:8000'
    });

    gulp.watch('app/static/sass/*.sass', ['compile-sass']);
    gulp.watch('app/static/js/**/*', browserSync.reload);
    gulp.watch('app/templates/**/*.html', browserSync.reload);
});

gulp.task('default', ['compile-sass', 'watch']);
