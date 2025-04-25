% convergence study plot
% from assignment: number of elements versus hole-center x-displacement
close all;  % close any existing figure windows

% add data
num_elements = [314 497 692 845];

% displacement (abs in negative x-direction, removed negative)
uh = [4.05137E-07 4.05891E-07 4.06373E-07 4.06413E-07];
uinfinity = 4.0643E-07;
g = 3.3117*10^-19;
alpha = 13.4141;

convergence = figure;   % create figure
figure(convergence);    % select fig
hold on;
plot(num_elements, uh, "r*", 'MarkerSize', 14);
plot(num_elements, uinfinity*ones(size(uh)), 'b--');
legend('Simulation Results', 'Estimated Solution u infinity', 'Location', 'southeast')
xlabel('Number of Elements')
ylabel('Absolute Value of x-Displacement at Top Hole (mm)')
title('Convergence Study Results')
grid on

