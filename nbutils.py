import math
import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip
import skimage.io
import glob
from IPython import display
import os


def display_images(image_paths, columns=1,width=800,title=None,headings=None,show_filenames=True):
    '''
    displays table of images given by list of image_paths in the Jupyter notebook
    
    Parameters
    ----------
    image_paths : list of paths to image files
    columns : number of colums to display
    width : total number of pixels for entire table
    title : optional title to display
    headings : optional list of headings for columns
    '''
    column = 0
    html = ''
    if title is not None:
        html = "<b>{0}</b>".format(title)
    html += "<table><tr>"
    if headings is not None:
        for heading in headings:
            html+="<td><b>{0}</b></td>".format(heading)
        html += "</tr><tr>"
    for image_path in image_paths:
        column += 1
        if column > columns:
            column = 1
            html += "</tr><tr>"
        html += "<td>"
        html += "<a href={0}?{r} target='_blank'>".format(image_path,r=np.random.randint(1000000))
        html += "<img width={size} height={size} src='{0}?{r}'>".format(
            image_path,size=width//columns,r=np.random.randint(1000000))
        html += "</a>"
        if show_filenames:
            html += "<a href={0}?{r} target='_blank'>{0}</a>".format(
                image_path,r=np.random.randint(1000000))
        html += "</td>"
    
    html += "</tr></table>"
    display.display(display.HTML(html))

    
def video_tag(path,width=300,height=240,title=""):
    '''
    generates an HTML fragmentfor displaying the video in path in the notebook
    '''
    return """
    <div style="float:left;padding-left:5px">
    <p>{3}</p>
    <video width="{1}" height="{2}" controls>
      <source src="{0}" type="video/mp4">
    </video>
    </div>
    """.format(path,width,height,title)

def display_video(video_path, **kwargs):
    html = video_tag(video_path, title=video_path, **kwargs)
    display.display(display.HTML(html))
    
def process_images(input_images, process_function, prefix, output_folder = 'output_images', overwrite=True, plot=False):
    '''
    Helper function that will process images according to a process function
    
    Returns
    -------
    list of processed images
    '''
    output_paths = []
    for input_path in input_images:
        output_path = output_folder+"/"+prefix+os.path.basename(input_path)
        output_paths.append(output_path)
        if overwrite or not os.path.exists(output_path):
            im=cv2.cvtColor(cv2.imread(input_path),cv2.COLOR_BGR2RGB)
            im_processed = process_function(im)
            plt.imsave(output_path,im_processed)
        
        if plot:
            fig = plt.figure()
            fig.set_size_inches(w=10,h=5)
            plt.subplot(1,2,1)
            plt.title(input_path)
            plt.imshow(im)
            plt.subplot(1,2,2)
            plt.title(output_path)
            plt.imshow(im_processed,cmap='gray')
    return output_paths