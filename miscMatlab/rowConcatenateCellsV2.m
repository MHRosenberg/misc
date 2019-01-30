function [datTab_selTrl_uniqueCellRows, datCell_selTrl_uniqueCellRows] = rowConcatenateCells(dataTable_selectedTrials)


datTab_selTrl_uniqueCellRows = {};

priorInds = 0;
numMice = numel(unique(dataTable_selectedTrials.mouse));
for mouseInd = 1:numMice
    numSessions = numel(unique(dataTable_selectedTrials.session));
    for sessionInd = 1:numSessions
        allStimuliNames = unique(dataTable_selectedTrials.stim);
        numStimTypes = numel(allStimuliNames);
        
        for stimTypeInd = 1:numStimTypes
            % find indices of the cells that are the same across trials 
            trialInds_selected_mouse = find(ismember(dataTable_selectedTrials.mouse,mouseInd));
            trialInds_selectedSession = find(ismember(dataTable_selectedTrials.session,sessionInd));
            trialInds_selectedStim = find(ismember(dataTable_selectedTrials.stim,allStimuliNames{stimTypeInd}));
            trialInds_sameCell_sameStim = intersect(intersect(trialInds_selected_mouse,trialInds_selectedSession),trialInds_selectedStim);

            % 
            tempTable = dataTable_selectedTrials(trialInds_sameCell_sameStim,:);
            for trialInd = 1:height(tempTable)
                stimInds_onsetOffset = tempTable.annot(1,1).stim.stim_on;
                timeInd_start = stimInds_onsetOffset(1);
                timeInd_end = stimInds_onsetOffset(2);
                
                if trialInd == 1
                    tempTable.rast{1} = tempTable.rast{2};
                end
            end
            tempCell = table2cell(tempTable);

            try tempCell(1,:)
                datCell_selTrl_uniqueCellRows(stimTypeInd+priorInds,:) = tempCell(1,:);  
                clear tempCell
            catch
                disp(['stim type: ' allStimuliNames{stimTypeInd} ' in this session --> skipping'])
            end
            clear tempCell
        end
        priorInds = priorInds + numStimTypes;
    end
end
datCell_selTrl_uniqueCellRows(all(cellfun('isempty',datCell_selTrl_uniqueCellRows),2),:) = [];
datTab_selTrl_uniqueCellRows = cell2table(datCell_selTrl_uniqueCellRows,'VariableNames', {'date','mouse','session','trial','stim', 'CaFR', ...
    'annoFR', 'rast','CaTime', 'rast_matched', 'match', 'units', 'bounds', 'io', 'annot','annoTime'});
