
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

a = ones(NUM_COMPARED,1) * 0.35;
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
clear
% lambda = 0.42; %0.42 for 0.75 mL
% a = linspace(0,1,10)';

NUM_COMPARED = 5;
NUM_REWARDS = 3;

a = ones(NUM_COMPARED,1) * 0.15;
b = linspace(0.1,0.4,NUM_COMPARED)';
x = linspace(1,NUM_REWARDS,NUM_REWARDS)';
y = b * log(x'+1);

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
