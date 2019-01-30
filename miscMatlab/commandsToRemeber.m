setdiff

intersect

interp

plot(timex,ycompression*mean(wavesinchani)+zchan,'Color',[0.2,0.2,0.2],'LineWidth',0.5)

line([etime/60 etime/60], [0 ceil(1.1*max(psthuniti))],'Color','r','LineStyle','-')  %convert times to minutes
            text(etime/60,1.05*max(psthuniti),[' \leftarrow' eventannotations{events}],'FontSize',8)
            
            spectrogram
            
            fliplr
            
            patch
            
            
            
            
            t=linspace(0,6,180)-WIN_SIZE_IN_FRAMES/FRAMES_PER_SEC;
            plot(t,smooth(nanmean(data{fileInd,3}(:,firstLoomPlotted:lastLoomAvailable),2),smoothSpan,'moving')) % plot first meaned loom episodes
            subplot(3,1,3)
    smoothSpan = 15;
    display(fileInd)
    plot(t,smooth(nanmean(data{fileInd,3}(:,1:end),2), smoothSpan ,'moving')) % plot ALL meaned loom episodes
    box off;
    hold on;
    maxY = ylim;
    maxY = maxY(2);
    plot([0 0],[0 maxY]);
    title([data{fileInd,1} ' plotted avg of all ' num2str(size(data{fileInd,3},2)) ' looms'])
    xlim([t(1) t(end)]);
    ylim([0 maxY]);
    set(gca,'Xtick', -3:0.5:3)