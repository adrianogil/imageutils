alias dip-list-images='python2 $IMAGE_UTILS_DIR/list_images.py'
alias dip-switch-color='python3 $IMAGE_UTILS_DIR/python/dip/switch_color.py'
alias dip-switch-color-dist='python3 $IMAGE_UTILS_DIR/python/dip/switch_color_distance.py'
alias dip-histogram='python3 $IMAGE_UTILS_DIR/python/dip/color_histogram.py'
alias dip-crop='python3 $IMAGE_UTILS_DIR/python/dip/crop.py'
alias dip-grid='python3 $IMAGE_UTILS_DIR/python/dip/grid.py'

# @tool dip-show-colors-in-point-cloud shows an image as a color point cloud in RGB space
# You need to setup first a html hosting at repo folder
# https://github.com/yig/image-rgb-in-3D
function dip-show-colors-in-point-cloud()
{
    target_image=$1
    current_dir=$PWD

    cp $target_image $COLORS_IN_POINT_CLOUD_DIR/target_images/

    open http://localhost:5353?image=target_images/$target_image
}
