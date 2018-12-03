function [Settings,patterns] = nordif2hdf5(DATFilename)
% nordif2hdf5 Read Kikuchi diffraction patterns from a DAT-file output by
% the Nordif software and write these patterns to an HDF5-file.
%
% The script assumes that your Setting.txt file is named exactly that, and
% that it is located in the same directory as you Pattern.dat file.
%
% Assumes you can have your full dataset in memory! Will look at a smarter
% solution in the future.
% 
% Parameters
% DATFilename : path. Full file path of DAT-file output from Nordif
%
% Returns
% Settings : struct. Structure with grid dimensions and pattern size
% patterns : array. Matrix of diffraction patterns
%
% Håkon Wiik Ånes (hakon.w.anes@ntnu.no)
% 2018-11-06

% Check if input file is a DAT-file
[filepath,filename,ext] = fileparts(DATFilename);
if ~strcmp(ext,'.dat')
    error('This is not a DAT-file.')
end

% Read settings file
settingsFile = fullfile(filepath,'Setting.txt');
text = textread(settingsFile,'%s','delimiter','\n');

% Find pixel size of patterns in file
acquisitionOccurence = regexp(text,'Acquisition settings'); % Find expression
acquisitionRow = find(~cellfun(@isempty,acquisitionOccurence)); % Find line
patternSizeString = textscan(text{acquisitionRow + 2},'%s'); % Read line
patternSizeString = strsplit(patternSizeString{1}{2},'x'); % Split string
Settings.PATTERNWIDTH = str2double(patternSizeString{1});
Settings.PATTERNHEIGHT = str2double(patternSizeString{2});

% Find grid dimensions in file
areaOccurence = regexp(text,'Area','match');
areaRow = find(~cellfun(@isempty,areaOccurence));
numberOfSamplesString = textscan(text{areaRow + 6},'%s');
interestingPartOfString = strsplit(numberOfSamplesString{1}{4},'x');
Settings.NCOLS = str2num(interestingPartOfString{1});
Settings.NROWS = str2num(interestingPartOfString{2});

% Read patterns from file
fid = fopen(DATFilename);
patterns = fread(fid,'*uint8');

% Shape (size) of data matrix
matrixShape = [Settings.PATTERNWIDTH,Settings.PATTERNHEIGHT,Settings.NCOLS,...
    Settings.NROWS];

% Reshape patterns into 4D array
patterns = reshape(patterns,matrixShape);

% Create an HDF5 file
hdf5Filename = fullfile(filepath,[filename '.h5']);
datasetName = '/data';
h5create(hdf5Filename,datasetName,size(patterns),'datatype','uint8');

% Write data to this file
h5write(hdf5Filename,datasetName,patterns);

end