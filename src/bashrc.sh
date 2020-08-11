alias dip-list-images='python3 $IMAGE_UTILS_DIR/list_images.py'
alias dip-switch-color='python3 $IMAGE_UTILS_DIR/python/dip/switch_color.py'
alias dip-switch-color-dist='python3 $IMAGE_UTILS_DIR/python/dip/switch_color_distance.py'
alias dip-histogram='python3 $IMAGE_UTILS_DIR/python/dip/color_histogram.py'
alias dip-crop='python3 $IMAGE_UTILS_DIR/python/dip/crop.py'
alias dip-grid='python3 $IMAGE_UTILS_DIR/python/dip/grid.py'

function dip-gen-icns-from-img()
{
    target_image_file=$1

    mkdir MyIcon.iconset
    sips -z 16 16     ${target_image_file} --out MyIcon.iconset/icon_16x16.png
    sips -z 32 32     ${target_image_file} --out MyIcon.iconset/icon_16x16@2x.png
    sips -z 32 32     ${target_image_file} --out MyIcon.iconset/icon_32x32.png
    sips -z 64 64     ${target_image_file} --out MyIcon.iconset/icon_32x32@2x.png
    sips -z 128 128   ${target_image_file} --out MyIcon.iconset/icon_128x128.png
    sips -z 256 256   ${target_image_file} --out MyIcon.iconset/icon_128x128@2x.png
    sips -z 256 256   ${target_image_file} --out MyIcon.iconset/icon_256x256.png
    sips -z 512 512   ${target_image_file} --out MyIcon.iconset/icon_256x256@2x.png
    sips -z 512 512   ${target_image_file} --out MyIcon.iconset/icon_512x512.png
    iconutil -c icns MyIcon.iconset
    rm -R MyIcon.iconset
}


function dip-background-transparent()
{
    target_image=$1
    output_image=$2

    convert ${target_image} -transparent white ${output_image}
}


# @tool dip-show-colors-in-point-cloud shows an image as a color point cloud in RGB space
# You need to setup first a html hosting at repo folder
# https://github.com/yig/image-rgb-in-3D
function dip-show-colors-in-point-cloud()
{
    target_image=$1
    current_dir=$PWD
    target_port=5353

    cp $target_image $COLORS_IN_POINT_CLOUD_DIR/target_images/

    cd $COLORS_IN_POINT_CLOUD_DIR
    simple-server ${target_port}

    cd ${current_dir}

    open http://localhost:${target_port}?image=target_images/${target_image}
}

function dip-gif-frame-reduce()
{
    # This script will take an animated GIF and delete every other frame
    # Accepts two parameters: input file and output file
    # Usage: ./<scriptfilename> input.gif output.gif

    # Make a copy of the file
    cp $1 $2

    # Get the number of frames
    numframes=`gifsicle $1 -I | ggrep -P "\d+ images" --only-matching | ggrep -P "\d+" --only-matching`

    # Deletion
    let i=0
    while [[ $i -lt $numframes  ]]; do
        rem=$(( $i % 2 ))

        if [ $rem -eq 0 ]
        then
            gifsicle $2 --delete "#"$(($i/2)) -o $2
        fi

        let i=i+1
    done
}
