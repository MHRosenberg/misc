% exponential increasing rewards (separate slope commands)
clear
% lambda = 0.42; %0.42 for 0.75 mL
% a = linspace(0,1,10)';

NUM_COMPARED = 5;
NUM_REWARDS = 5;
LOWEST_MAX_REWARD = 0.76;
HIGHEST_MAX_REWARD = 1.36;
TOLERANCE = 0.001;
MOD_SIZE = 0.00001;

lowestStart = 0.5;
highestStart = 0.5;
lowFinished = 0;
highFinished = 0;
iteration = 1;
while lowFinished == 0 || highFinished == 0
    a = ones(NUM_COMPARED,1) * 0.15;
    b = linspace(lowestStart,highestStart,NUM_COMPARED)';
    x = linspace(1,NUM_REWARDS,NUM_REWARDS)';
    y = b * log(x'+1);
    cumSum = cumsum(y,2);
%     disp(y)
    disp(cumSum)
    disp(iteration)
    
    %%% check highest value
    if abs(cumSum(end)-HIGHEST_MAX_REWARD) < TOLERANCE 
        highFinished = 1;
       disp('high finished')
    elseif cumSum(end) > HIGHEST_MAX_REWARD
        highestStart = highestStart - MOD_SIZE;
    elseif cumSum(end) < HIGHEST_MAX_REWARD
        highestStart = highestStart + MOD_SIZE;
    end
        
    %%% check lowest value
    if abs(cumSum(1,end)-LOWEST_MAX_REWARD) < TOLERANCE 
        lowFinished = 1; 
       disp('low finished')
    elseif cumSum(1,end) > LOWEST_MAX_REWARD 
        lowestStart = lowestStart - MOD_SIZE;
    elseif cumSum(1,end) < LOWEST_MAX_REWARD
        lowestStart = lowestStart + MOD_SIZE;
    end
    iteration = iteration + 1;
end


close all
f = figure();
hold on

% h = zeros(2,1);
% h(1) = plot(x,y, 'o');
% h(2) = plot(x,cumsum(y), 's');

% plot(x,y,'o', 'MarkerFaceColor', 'b')
% plot(x,cumsum(y),'o', 'MarkerFaceColor', 'r')

plot(x,y, 'Marker', 's', 'MarkerFaceColor' , 'red');
plot(x, cumsum(y,2), 'Marker', 'o', 'MarkerFaceColor' , 'blue');

legend('reward qty delivered', 'cumuulative reward')
% title(['lambda = ' num2str(lambda)])
xlabel('reward number')
ylabel('mL')
grid on
grid minor
