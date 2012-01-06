% test_example.m
% 测试路网的绘图
% 崔亚平

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear;clc;
close all;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 导入道路采样位置
node_table = load('node table.txt'); % 第三列为x坐标，第四列为y坐标
road.position = node_table(:,[2:3]); % 节点的x、y坐标

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 道路可视化

% figure;
% plot(road.position(:,1),road.position(:,2),'.g'); % 离散的采样点
% 
% figure;
% plot(road.position(:,1),road.position(:,2),'r');  % 连续的

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 示例道路
[position] = road_sample();

figure;
plot(position.beltlinehwy2(:,1),position.beltlinehwy2(:,2),'k');
hold on;
plot(position.beltlinehwy1(:,1),position.beltlinehwy1(:,2),'b');
hold on;
plot(position.bassettst(:,1),position.bassettst(:,2),'r');
hold on;
plot(position.blairst1(:,1),position.blairst1(:,2),'y');
hold on;
plot(position.blairst2(:,1),position.blairst2(:,2),'m');
hold on;
plot(position.c2(:,1),position.c2(:,2),'b');
hold on;
plot(position.c3(:,1),position.c3(:,2),'r');
hold on;
plot(position.cordman(:,1),position.cordman(:,2),'m');
hold on;
plot(position.c1(:,1),position.c1(:,2),'c');
hold on;
plot(position.dinave(:,1),position.dinave(:,2),'g');
hold on;
plot(position.fishhatehurryrd1(:,1),position.fishhatehurryrd1(:,2),'r');
hold on;
plot(position.fishhatehurryrd2(:,1),position.fishhatehurryrd2(:,2),'b');
hold on;
plot(position.gorhamst(:,1),position.gorhamst(:,2),'g');
hold on;
plot(position.johnnolendr(:,1),position.johnnolendr(:,2),'c');
hold on;
plot(position.mineralpointrd(:,1),position.mineralpointrd(:,2),'k');
hold on;
plot(position.monvoest(:,1),position.monvoest(:,2),'b');
hold on;
plot(position.odanard(:,1),position.odanard(:,2),'c');
hold on;
plot(position.oldmiddletonrd(:,1),position.oldmiddletonrd(:,2),'g');
hold on;
plot(position.proudfitst(:,1),position.proudfitst(:,2),'b');
hold on;
plot(position.raymondrd(:,1),position.raymondrd(:,2),'g');
hold on;
plot(position.sgammonrd(:,1),position.sgammonrd(:,2),'k');
hold on;
plot(position.sparkst1(:,1),position.sparkst1(:,2),'k');
hold on;
plot(position.sparkst2(:,1),position.sparkst2(:,2),'g');
hold on;
plot(position.universityave1(:,1),position.universityave1(:,2),'g');
hold on;
plot(position.universityave2(:,1),position.universityave2(:,2),'c');
hold on;
plot(position.universityave3(:,1),position.universityave3(:,2),'r');
hold on;
plot(position.universityave4(:,1),position.universityave4(:,2),'r');
hold on;
plot(position.universityave5(:,1),position.universityave5(:,2),'b');
hold on;
plot(position.universityave6(:,1),position.universityave6(:,2),'y');
hold on;
plot(position.universityave7(:,1),position.universityave7(:,2),'b');
hold on;
plot(position.wbadgerrd(:,1),position.wbadgerrd(:,2),'k');
hold on;
plot(position.whiteneyway1(:,1),position.whiteneyway1(:,2),'g');
hold on;
plot(position.whiteneyway2(:,1),position.whiteneyway2(:,2),'b');
hold on;
plot(position.whiteneyway3(:,1),position.whiteneyway3(:,2),'g');
hold on;
plot(position.b1(:,1),position.b1(:,2),'r');
hold on;
plot(position.b2(:,1),position.b2(:,2),'r');
hold on;
plot(position.b3(:,1),position.b3(:,2),'r');
hold on;
plot(position.b4(:,1),position.b4(:,2),'r');
hold on;
plot(position.b5(:,1),position.b5(:,2),'r');
hold on;
plot(position.b6(:,1),position.b6(:,2),'r');
hold on;
plot(position.b7(:,1),position.b7(:,2),'r');
hold on;
plot(position.a1(:,1),position.a1(:,2),'r');
hold on;
plot(position.a2(:,1),position.a2(:,2),'r');
hold on;
plot(position.a3(:,1),position.a3(:,2),'r');
hold on;
plot(position.a4(:,1),position.a4(:,2),'r');
hold on;
plot(position.a5(:,1),position.a5(:,2),'r');
hold on;
plot(position.a6(:,1),position.a6(:,2),'r');
hold on;
plot(position.a7(:,1),position.a7(:,2),'r');
hold on;
plot(position.a8(:,1),position.a8(:,2),'r');
hold on;
plot(position.a9(:,1),position.a9(:,2),'r');
hold on;
plot(position.a10(:,1),position.a10(:,2),'r');
hold on;
plot(position.a11(:,1),position.a11(:,2),'r');
hold on;
plot(position.a12(:,1),position.a12(:,2),'r');
hold on;
plot(position.a13(:,1),position.a13(:,2),'r');
hold on;
plot(position.a14(:,1),position.a14(:,2),'r');
hold on;
plot(position.a15(:,1),position.a15(:,2),'r');
hold on;
plot(position.a16(:,1),position.a16(:,2),'r');
hold on;
plot(position.a17(:,1),position.a17(:,2),'r');
hold on;
plot(position.a18(:,1),position.a18(:,2),'r');
hold on;
plot(position.a19(:,1),position.a19(:,2),'r');
hold on;
plot(position.a20(:,1),position.a20(:,2),'r');
hold on;
plot(position.a21(:,1),position.a21(:,2),'r');
hold on;
plot(position.a22(:,1),position.a22(:,2),'r');
hold on;
plot(position.a23(:,1),position.a23(:,2),'r');
hold on;
plot(position.a24(:,1),position.a24(:,2),'r');
hold on;
plot(position.a25(:,1),position.a25(:,2),'r');
hold on;
plot(position.a26(:,1),position.a26(:,2),'r');
hold on;
plot(position.a27(:,1),position.a27(:,2),'r');
hold on;
plot(position.a28(:,1),position.a28(:,2),'r');
hold on;
plot(position.a29(:,1),position.a29(:,2),'r');
hold on;
plot(position.a30(:,1),position.a30(:,2),'r');
hold on;
plot(position.a31(:,1),position.a31(:,2),'r');
hold on;
plot(position.a32(:,1),position.a32(:,2),'r');
hold on;
plot(position.a33(:,1),position.a33(:,2),'r');
hold on;
plot(position.a34(:,1),position.a34(:,2),'r');
hold on;
plot(position.a35(:,1),position.a35(:,2),'r');
hold on;
plot(position.a36(:,1),position.a36(:,2),'r');
hold on;
plot(position.a37(:,1),position.a37(:,2),'r');
hold on;
plot(position.a38(:,1),position.a38(:,2),'r');
hold on;
plot(position.a39(:,1),position.a39(:,2),'r');
hold on;
plot(position.a41(:,1),position.a41(:,2),'r');
hold on;
plot(position.a40(:,1),position.a40(:,2),'r');
hold on;
plot(position.a42(:,1),position.a42(:,2),'r');
hold on;
plot(position.a43(:,1),position.a43(:,2),'r');
hold on;
plot(position.a44(:,1),position.a44(:,2),'r');
hold on;
plot(position.a45(:,1),position.a45(:,2),'r');
hold on;
plot(position.schroederrd(:,1),position.schroederrd(:,2),'b');
