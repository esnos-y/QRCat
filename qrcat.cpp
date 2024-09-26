// https://learnopencv.com/opencv-qr-code-scanner-c-and-python/
// https://learnopencv.com/barcode-and-qr-code-scanner-using-zbar-and-opencv/

#include <iostream>
#include <string>

#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <zbar.h>


int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "QRCat, dumps content of QR code." << std::endl;
        std::cerr << "Expected arguments: /path/to/image" << std::endl;
        return 1;
    }
    const char *image_path = argv[1];

    cv::Mat input_image = cv::imread(image_path, cv::IMREAD_GRAYSCALE);
    cv::imshow("Input image", input_image);
    cv::waitKey(0);

    zbar::ImageScanner scanner;
    scanner.set_config(zbar::ZBAR_NONE, zbar::ZBAR_CFG_ENABLE, 1);

    zbar::Image zbar_image(input_image.cols, input_image.rows, "Y800", input_image.data,
                           input_image.cols * input_image.rows);

    int n = scanner.scan(zbar_image);
    for (zbar::Image::SymbolIterator it = zbar_image.symbol_begin(); it != zbar_image.symbol_end(); ++it) {
        std::string type = it->get_type_name();
        std::string data = it->get_data();
        std::cout << "Type: " << type << std::endl;
        std::cout << "Data: " << data << std::endl;
    }

    return 0;
}
