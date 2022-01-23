 %load('gTruth_bueno.mat')
 x=gTruth.LabelData;
 x=table2array(x);

[fil,col]=size(x);
nuevo=[];
bool=1;%esta vacio
for i=1:fil
    j=1;
    bool=1;
    while (bool==1 && j~=col) %look if the row has any element, if it has, we save it. 
        bool=isempty(x{i,j});
        j=j+1;
    end
    if bool==0
        nuevo=[nuevo;x(i,:)];
    end
    disp(i)
end


%dividimos en train y test
train=nuevo(501:1500,:);
test_1=nuevo(1:500,:);
test_2=nuevo(1501:1548,:);
test=[test_1;test_2];

