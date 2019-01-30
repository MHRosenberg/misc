
%% exponential rewards (common lambda)
clear
% lambda = 0.42; %0.42 for 0.75 mL
lambda = linspace(0.3,0.6,10)';
x = linspace(1,4,4)';
y = lambda' .* exp(-lambda * (x'-1))';


close all
hold on
% plot(x,y,'o', 'MarkerFaceColor', 'b')
plot(x,y);
% plot(x,cumsum(y),'o', 'MarkerFaceColor', 'r')
plot(x,cumsum(y))
legend('reward qty delivered','cumuulative reward')
% title(['lambda = ' num2str(lambda)])
xlabel('reward number')
ylabel('mL')
grid on
grid minor

%% decreasing exponential rewards (separate slope commands)
clear
% lambda = 0.42; %0.42 for 0.75 mL
% a = linspace(0,1,10)';

NUM_COMPARED = 5;

a = ones(NUM_COMPARED,1) * 0.5;
b = linspace(0.1,0.3,NUM_COMPARED)';
% b = ones(10,1);
x = linspace(1,4,4)';
y = a' .* exp(-b * (x'-1))';

close all
f = figure();
hold on

% h = zeros(2,1);
% h(1) = plot(x,y, 'o');
% h(2) = plot(x,cumsum(y), 's');

% plot(x,y,'o', 'MarkerFaceColor', 'b')
% plot(x,cumsum(y),'o', 'MarkerFaceColor', 'r')

plot(x,y, 'o');
plot(x,cumsum(y), 's');

% legend(h, 'reward qty delivered', 'cumuulative reward')
% title(['lambda = ' num2str(lambda)])
xlabel('reward number')
ylabel('mL')
grid on
grid minor


%% exponential increasing rewards (separate slope commands)
% exponential increasing rewards (separate slope commands)
clear
% lambda = 0.42; %0.42 for 0.75 mL
% a = linspace(0,1,10)';

NUM_COMPARED = 4; 
NUM_REWARDS = 5; %%% MUST BE EVEN!
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


close all
f = figure();
hold on

% h = zeros(2,1);
% h(1) = plot(x,y, 'o');
% h(2) = plot(x,cumsum(y), 's');

% plot(x,y,'o', 'MarkerFaceColor', 'b')
% plot(x,cumsum(y),'o', 'MarkerFaceColor', 'r')

%%% transposed to enforce correct matlab ordering
y = y';
cumSum = cumSum';

plot(x,y, 'Marker', 's', 'MarkerFaceColor' , 'red');
plot(x, cumSum, 'Marker', 'o', 'MarkerFaceColor' , 'blue');

legend('reward qty delivered', 'cumuulative reward')
% title(['lambda = ' num2str(lambda)])
xlabel('reward number')
ylabel('mL')
grid on
grid minor


%% constant rewards
x = linspace(1,4,4);
y = x * 0 + 0.25;

close all 
hold on
plot(x,y,'o', 'MarkerFaceColor', 'b')
plot(x,cumsum(y),'o', 'MarkerFaceColor', 'r')
% legend('reward qty delivered','cumuulative reward')
% title(['lambda = ' num2str(lambda)])
xlabel('reward number')
ylabel('mL')
grid on
grid minor
