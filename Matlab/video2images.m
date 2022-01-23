function [] = video2images(videoFile, imageExt)
% Convert video file to a sequence of image files. 
% A new folder is created in the location of the video file with the same name. 
% 
% Inputs:
%  -videoFile: string containing the path and video file name.
%  -imageExt: string containing the image extension of the output sequence
%  of images.
% -------------------------------------------------------------------------

% Create a video file reader.
videoReader = vision.VideoFileReader(videoFile);

% Path of the video file.
[pathstr, name, ~] = fileparts(videoFile);
if(isempty(pathstr))
    pathstr = '.';
end
pathstr = [pathstr, '/'];

% Create folder with the same name as the video file.
mkdir([pathstr, name]);

i = 0;
while ~isDone(videoReader)
    frame = videoReader.step();
    str = sprintf('%s/%s/%09d.%s', pathstr, name, i, imageExt);
    imwrite(frame, str);
    i = i+1;
end
release(videoReader);