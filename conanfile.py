from conans import ConanFile, CMake, tools
import os


class OpencvConan(ConanFile):
    name = "opencv"
    version = "3.1.0"
    license = "MIT"
    url = "https://github.com/anishitani/conanio-opencv"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False]
    }
    default_options = "shared=True"
    generators = "cmake"

    def source(self):
        self.run("git clone --depth 1 https://github.com/opencv/opencv.git")
        self.run("cd opencv && git fetch origin " + self.version)

    def build(self):
        cmake = CMake(self.settings)
        flags = "-DWITH_IPP=OFF -DBUILD_EXAMPLES=OFF -DBUILD_DOCS=OFF -DBUILD_TESTS=OFF -DBUILD_opencv_apps=OFF -DBUILD_PERF_TESTS=OFF"
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake opencv %s %s %s' % (cmake.command_line, shared, flags))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h*", dst="include", src="opencv/include", keep_path=True)

        for lib in ["calib3d", "cudaarithm", "cudafeatures2d", "cudalegacy",
                    "cudastereo", "features2d", "imgcodecs", "ml", "superres",
                    "videoio", "world", "cudabgsegm", "cudafilters",
                    "cudaobjdetect", "cudawarping", "flann", "imgproc",
                    "objdetect", "shape", "ts", "videostab", "core", "cudacodec",
                    "cudaimgproc", "cudaoptflow", "cudev", "highgui", "photo",
                    "stitching", "video", "viz"]:
            self.copy("*.h*", "include", "opencv/modules/%s/include" %
                      (lib))

        self.copy("*.so", dst="lib", keep_path=False)

    # def package_info(self):
    #     self.cpp_info.libs = ["hello"]
