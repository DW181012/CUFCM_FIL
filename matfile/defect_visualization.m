selfname = 'ciliate_130fil_1600blob_1.00R_0.0500torsion_0.0000tilt_1.0000dp_0.0000noise_0.0000ospread';
%cd 20250225_pizza_demo3
cd ..
cd data
cd pizza_sim
cd 20250602_mcc_test

TRUE_STATES = importdata([selfname,'_true_states.dat']);
SEG_STATES = importdata([selfname,'_seg_states.dat']);
SEG_FORCES = importdata([selfname,'_seg_forces.dat']);
SEG_VELS = importdata([selfname,'_seg_vels.dat']);
FIL_REF = importdata([selfname,'_fil_references.dat']);
FIL_Q = importdata([selfname,'_fil_q.dat']);
BODY_STATES = importdata([selfname,'_body_states.dat']);

cd ..
cd ..
cd ..

M = size(FIL_REF,2)/3;
clock = TRUE_STATES(:,1);
clockmax = clock(end);
clockstart = clock(1);
N_step = size(clock,1);
clockstep = (clockmax - clockstart) / (N_step - 1);
NSEG = (size(SEG_STATES,2) - 1) ./ (3 .* M);
Y1 = zeros(M,NSEG);
Y2 = zeros(M,NSEG);
Y3 = zeros(M,NSEG);

psi = zeros(N_step,M);
theta = zeros(N_step,M);
Y_seg = zeros(N_step,M,NSEG,3);
f_seg = zeros(N_step,M,NSEG,3);
t_seg = zeros(N_step,M,NSEG,3);
vel_seg = zeros(N_step,M,NSEG,3);
rot_seg = zeros(N_step,M,NSEG,3);
root = zeros(M,3);
q_fil = zeros(M,4);
r_body = zeros(N_step,3);
q_body = zeros(N_step,4);

for m = 1 : M
    root(m,:) = FIL_REF(3 * m - 2 : 3 * m);
    q_fil(m,:) = FIL_Q(4 * m - 3 : 4 * m);
end

figure(1)
viewangle1 = 18;
viewangle2 = 72;
filename = [selfname,num2str(viewangle1),num2str(viewangle2)];
cm = colormap(hsv(360));
set(figure(1), 'Position', [1 1 800 800])
for n = 1 : N_step
    time = clock(n);
    psi(n,:) = TRUE_STATES(n,3:2+M);
    theta = TRUE_STATES(n,M+3:(2*M+2));

    for m = 1 : M
        for nseg = 1 : NSEG
            index = (m - 1) * NSEG + nseg;
            Y_seg(n,m,nseg,:) = SEG_STATES(n,index * 3 - 1 : index * 3 + 1);
            f_seg(n,m,nseg,:) = SEG_FORCES(n,index * 6 - 4 : index * 6 - 2);
            t_seg(n,m,nseg,:) = SEG_FORCES(n,index * 6 - 1 : index * 6 + 1);
            vel_seg(n,m,nseg,:) = SEG_VELS(n,index * 6 - 4 : index * 6 - 2);
            rot_seg(n,m,nseg,:) = SEG_VELS(n,index * 6 - 1 : index * 6 + 1);
            Y1(m,nseg) = Y_seg(n,m,nseg,1);
            Y2(m,nseg) = Y_seg(n,m,nseg,2);
            Y3(m,nseg) = Y_seg(n,m,nseg,3);
        end

        phase_color = cm(floor(1+mod(psi(n,m),2*pi) * 360./(2*pi)),:);
        plot3(Y1(m,:),Y2(m,:),Y3(m,:),'-','color', phase_color,'MarkerSize',7);
        hold on
    end

    r_body(n,:) = BODY_STATES(n,2:4);
    q_body(n,:) = BODY_STATES(n,5:8);

    hold off

    xlabel('X','FontSize', 18)
    ylabel('Y','FontSize', 18)
    zlabel('Z','FontSize', 18)

    axis equal
    axis ([0 120 0 120 -10 110])
    title(['pizza t=' num2str(time)],'FontSize', 18)
    clim([0 360])
    colorbar('Ticks',[0 60 120 180 240 300 360],'TickLabels',{'$0$','$\frac{\pi}{3}$','$\frac{2\pi}{3}$','$\pi$','$\frac{4\pi}{3}$','$\frac{5\pi}{3}$','$2\pi$'},'TickLabelInterpreter','latex')
    view([viewangle1,viewangle2])

    drawnow

    if n == 1
        writegif([filename,'.gif'],1,10,1)
    else
        writegif([filename,'.gif'],0,10,1)
    end

    hold off
end

movefile([filename,'.gif'], 'gif');