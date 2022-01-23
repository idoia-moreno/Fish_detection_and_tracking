% load('gtruth_v2.mat')
% x=gTruth.LabelData;
% x=table2array(x);

%ejecutar antes script: 'dividirEnSecuencias.m'
x=test;

%para acceder a la posicion:

% x{1,1}.Position
% x{1,1}.ID

[fil,col]=size(x);
gTruth_Matrix=[]; %we initializa the matrix that will be our final gTruth at 1
%so that the last for values on each row are already 1.
new_row_vector=[];
for j=1:col  
    for i=1:fil
        empty=isempty(x{i,j}); %devuelve un 1 si esta vacio
        if empty==0
            id=x{i,j}.ID;
            position=x{i,j}.Position;
            position=round(position);
            new_row_vector=[i,id,position,1,1,1];
            gTruth_Matrix=[gTruth_Matrix;new_row_vector];       
        end
    end
end

writematrix(gTruth_Matrix,'gt_test.txt') 