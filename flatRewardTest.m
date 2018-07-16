clear
close all
%%% constant rewards


NUM_COMPARED = 4; 
NUM_REWARDS = 3; %%% MUST BE EVEN!
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
    y = x'* 0 + b;
    cumSum = cumsum(y,2);
%     disp(y)
    disp(cumSum)
    disp(iteration)
    
    %%% check highest value
    if abs(cumSum(end,end)-HIGHEST_MAX_REWARD) < TOLERANCE 
        highFinished = 1;
       disp('high finished')
    elseif cumSum(end,end) > HIGHEST_MAX_REWARD
        highestStart = highestStart - MOD_SIZE;
    elseif cumSum(end,end) < HIGHEST_MAX_REWARD
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


y = y';
cumSum = cumSum';

plot(x,y, 'Marker', 's', 'MarkerFaceColor' , 'red');
hold on
plot(x, cumSum, 'Marker', 'o', 'MarkerFaceColor' , 'blue');

legend('reward qty delivered', 'cumuulative reward')
% title(['lambda = ' num2str(lambda)])
xlabel('reward number')
ylabel('mL')
grid on
grid minor