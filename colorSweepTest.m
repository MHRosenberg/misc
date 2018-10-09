colors = colormap('jet');

figure(3)
hold on
for i =1:length(colors);
    plot([0 i], [1 5], 'color', colors(i,:));
    
end