
set(opencv_CXXFLAGS "-fstack-protector-all -Wno-maybe-uninitialized -Wno-unused-parameter -D_FORTIFY_SOURCE=2 -O2")
set(opencv_CFLAGS "-fstack-protector-all -Wno-maybe-uninitialized -Wno-unused-parameter -D_FORTIFY_SOURCE=2 -O2")
set(opencv_LDFLAGS "-Wl,-z,relro,-z,now,-z,noexecstack")

mindspore_add_pkg(opencv
        VER 4.2.0
        LIBS opencv_core opencv_imgcodecs opencv_imgproc
        URL https://github.com/opencv/opencv/archive/4.2.0.tar.gz
        MD5 e8cb208ce2723481408b604b480183b6
        CMAKE_OPTION -DCMAKE_BUILD_TYPE=Release -DWITH_PROTOBUF=OFF -DWITH_WEBP=OFF -DWITH_IPP=OFF -DWITH_ADE=OFF
        -DBUILD_ZLIB=ON
        -DBUILD_JPEG=ON
        -DBUILD_PNG=ON
        -DBUILD_OPENEXR=ON
        -DBUILD_TESTS=OFF
        -DBUILD_PERF_TESTS=OFF
        -DBUILD_opencv_apps=OFF
        -DCMAKE_SKIP_RPATH=TRUE
        -DBUILD_opencv_python3=OFF
        -DWITH_FFMPEG=OFF
        -DWITH_TIFF=ON
        -DBUILD_TIFF=OFF
        -DWITH_JASPER=OFF
        -DBUILD_JASPER=OFF
        -DTIFF_INCLUDE_DIR=${tiff_INC}
        -DTIFF_LIBRARY=${tiff_LIB})
include_directories(${opencv_INC}/opencv4)
add_library(mindspore::opencv_core ALIAS opencv::opencv_core)
add_library(mindspore::opencv_imgcodecs ALIAS opencv::opencv_imgcodecs)
add_library(mindspore::opencv_imgproc ALIAS opencv::opencv_imgproc)
