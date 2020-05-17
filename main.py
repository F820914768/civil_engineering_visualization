# =============================================================================
# Import related files
# =============================================================================

import structure as stu
import openseespy.opensees as ops
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import openseespy.postprocessing.Get_Rendering as opsplt 

# =============================================================================
# Import complete
# =============================================================================

if __name__ == '__main__':    
 
# =============================================================================
# 14 level frame
# =============================================================================

#    International unit: mm
    
    zoom = 1000
    l, b, h = 6*zoom, 8*zoom, 4*zoom
    span_L, span_B, level_H = 6, 3, 14
    
    frame_lvl_14 = stu.Frame(stu.axe)
    frame_lvl_14.add_storey(l, b, 5*zoom, span_L, span_B)
    
    for i in range(level_H - 1):
        frame_lvl_14.add_storey(l, b, h, span_L, span_B)
    
    frame_lvl_14.plot_range((0 , 40*zoom) , (0 , 30*zoom) , (0 , 60*zoom))
    frame_lvl_14.plot()
    
#    print(stu.node_manager.get_all)

# =============================================================================
#     
# =============================================================================
    
    nodeslist = stu.node_manager.get_all()

#    print(nodeslist)

    columns = frame_lvl_14.to_columns()
    
#    print(columns)
    
#    print(stu.node_manager.anti_get(129))
    
# =============================================================================
# clear ops Memory space    
# =============================================================================
    ops.wipe()
    
    print("\n已清空ops内存")
# =============================================================================
# create models    
# =============================================================================
    ops.model('basic', '-ndm', 3, '-ndf', 6)
    
    print("\n已创建模型空间")
# =============================================================================
# create nodes
# =============================================================================    
    for node_e in nodeslist:
        ops.node(*node_e)
        
    print("\n已创建节点")
# =============================================================================
# caculate parameters    
# =============================================================================    
    sum_material = 0
    for i in range(level_H):
        sum_material = sum_material + len(frame_lvl_14.to_columns_nth(i))
        sum_material = sum_material + len(frame_lvl_14.to_beamB_nth(i))
        sum_material = sum_material + len(frame_lvl_14.to_beamL_nth(i))

    print("\n" + "共" + str(sum_material) + "个单元")
    
    sum_beamB = 0
    for i in range(level_H):
        sum_beamB = sum_beamB + len(frame_lvl_14.to_beamB_nth(i))
    
    print("\n" + "共" + str(sum_beamB) + "个Beam-B单元")
    
    sum_beamL = 0
    for i in range(level_H):
        sum_beamL = sum_beamL + len(frame_lvl_14.to_beamL_nth(i))
        
    print("\n" + "共" + str(sum_beamL) + "个Beam-L单元")    

    sum_col = 0
    for i in range(level_H):
        sum_col = sum_col + len(frame_lvl_14.to_columns_nth(i))
    
    print("\n" + "共" + str(sum_col) + "个Column单元")    

# =============================================================================
# create material
# =============================================================================

#    International unit: mm . MPa

#   HT590:
    Fy_a = 490.0	        # STEEL yield stress
    Es_a = 1.57*10**5	    # modulus of steel
    Bs_a= 0.01		        # strain-hardening ratio 
    R0_a = 18.0		        # control the transition from elastic to plastic branches
    cR1_a = 0.925	        # control the transition from elastic to plastic branches
    cR2_a = 0.15		    # control the transition from elastic to plastic branches
#    uniaxialMaterial('Steel02', matTag, Fy, E0, b, *params, a1=a2*Fy/E0, 
#                       a2=1.0, a3=a4*Fy/E0, a4=1.0, sigInit=0.0)

    ops.uniaxialMaterial('Steel02', 1 , Fy_a, Es_a, Bs_a, R0_a , cR1_a , cR2_a)
    
    print("\n已创建框架柱材料")  

#   Q235B:
    Fy_b = 220.0	        # STEEL yield stress
    Es_b = 2.06*10**5	    # modulus of steel
    Bs_b = 0.01		        # strain-hardening ratio 
    R0_b = 18.0		        # control the transition from elastic to plastic branches
    cR1_b = 0.925	        # control the transition from elastic to plastic branches
    cR2_b = 0.15		    # control the transition from elastic to plastic branches
#    uniaxialMaterial('Steel02', matTag, Fy, E0, b, *params, a1=a2*Fy/E0, 
#                       a2=1.0, a3=a4*Fy/E0, a4=1.0, sigInit=0.0)

    ops.uniaxialMaterial('Steel02', 2 , Fy_b, Es_b, Bs_b, R0_b , cR1_b , cR2_b)
    
    print("\n已创建框架梁材料") 
    
# =============================================================================
# text(Debug) Material:    
# =============================================================================

#    text Material:
#    uniaxialMaterial('Elastic', matTag, E, eta=0.0, Eneg=E)
#    ops.uniaxialMaterial('Elastic', 2, E, 0.0, E)

# =============================================================================
# create section for columns from level 01 to level 05
# =============================================================================
    
#   patch('rect', matTag, numSubdivY, numSubdivZ, *crdsI, *crdsJ)
#   section('Fiber', secTag, '-torsion', torsionMatTag)        
    import section as section

#    International unit: mm
    
#    lvl_01_05_col = section.HSection(600, 600, 600, 30, 30, 30)   
    lvl_01_05_col = section.RectSection(600 , 600 , 30 , 30 , 30 , 30)
    lvl_01_05_col.plot()
    
    col_area_01_05 = lvl_01_05_col.compute_area()
    
#   get main point for bottom flange
    lvl_01_05_col_point_bottom_I = lvl_01_05_col.low_flange_main_point_1
    lvl_01_05_col_point_bottom_J = lvl_01_05_col.low_flange_main_point_2
    
#   get main point for top flange
    lvl_01_05_col_point_top_I = lvl_01_05_col.top_flange_main_point_1
    lvl_01_05_col_point_top_J = lvl_01_05_col.top_flange_main_point_2
         
#   get main point for left web
    lvl_01_05_col_point_web_left_I = lvl_01_05_col.web_main_left_point_1
    lvl_01_05_col_point_web_left_J = lvl_01_05_col.web_main_left_point_2

#   get main point for right web
    lvl_01_05_col_point_web_right_I = lvl_01_05_col.web_main_right_point_1
    lvl_01_05_col_point_web_right_J = lvl_01_05_col.web_main_right_point_2             
             
#   opensees section:   
    ops.section('Fiber', 1, '-torsion', 1)
    
    ops.patch("rect" , 1 , 5 , 1 , *lvl_01_05_col_point_bottom_I ,
              *lvl_01_05_col_point_bottom_J)
    ops.patch("rect" , 1 , 5 , 1 , *lvl_01_05_col_point_top_I , 
              *lvl_01_05_col_point_top_J)
    ops.patch("rect" , 1 , 1 , 5 , *lvl_01_05_col_point_web_left_I , 
              *lvl_01_05_col_point_web_left_J)
    ops.patch("rect" , 1 , 1 , 5 , *lvl_01_05_col_point_web_right_I , 
              *lvl_01_05_col_point_web_right_J)
    
    print("\n01-05层柱截面创建完毕")
    
# =============================================================================
# create section for columns from level 06 to level 10
# =============================================================================

#   patch('rect', matTag, numSubdivY, numSubdivZ, *crdsI, *crdsJ)
#   section('Fiber', secTag, '-torsion', torsionMatTag)    

#    International unit: mm   
    
#    lvl_06_10_col = section.HSection(550, 550, 550, 24, 24, 24)
    lvl_06_10_col = section.RectSection(550 , 550 , 24 , 24 , 24 , 24)
    lvl_06_10_col.plot()
    
    col_area_06_10 = lvl_06_10_col.compute_area()

#   get main point for bottom flange
    lvl_06_10_col_point_bottom_I = lvl_06_10_col.low_flange_main_point_1
    lvl_06_10_col_point_bottom_J = lvl_06_10_col.low_flange_main_point_2
    
#   get main point for top flange
    lvl_06_10_col_point_top_I = lvl_06_10_col.top_flange_main_point_1
    lvl_06_10_col_point_top_J = lvl_06_10_col.top_flange_main_point_2
         
#   get main point for left web
    lvl_06_10_col_point_web_left_I = lvl_06_10_col.web_main_left_point_1
    lvl_06_10_col_point_web_left_J = lvl_06_10_col.web_main_left_point_2 
    
#   get main point for right web
    lvl_06_10_col_point_web_right_I = lvl_06_10_col.web_main_right_point_1
    lvl_06_10_col_point_web_right_J = lvl_06_10_col.web_main_right_point_2            
             
#   opensees section:   
    ops.section('Fiber', 2, '-torsion', 1)
    
    ops.patch("rect" , 1 , 5 , 1 , *lvl_06_10_col_point_bottom_I ,
              *lvl_06_10_col_point_bottom_J)
    ops.patch("rect" , 1 , 5 , 1 , *lvl_06_10_col_point_top_I , 
              *lvl_06_10_col_point_top_J)
    ops.patch("rect" , 1 , 1 , 5 , *lvl_06_10_col_point_web_left_I , 
              *lvl_06_10_col_point_web_left_J)
    ops.patch("rect" , 1 , 1 , 5 , *lvl_06_10_col_point_web_right_I , 
              *lvl_06_10_col_point_web_right_J)
        
    print("\n06-10层柱截面创建完毕")
    
# =============================================================================
# create section for columns from level 11 to level 14
# =============================================================================    

#   patch('rect', matTag, numSubdivY, numSubdivZ, *crdsI, *crdsJ)
#   section('Fiber', secTag, '-torsion', torsionMatTag)     

#    International unit: mm
    
#    lvl_11_14_col = section.HSection(500, 500, 500, 20, 20, 20)
    lvl_11_14_col = section.RectSection(500 , 500 , 20 , 20 , 20 , 20)
    lvl_11_14_col.plot()
    
    col_area_11_14 = lvl_11_14_col.compute_area()
    
#   get main point for bottom flange
    lvl_11_14_col_point_bottom_I = lvl_11_14_col.low_flange_main_point_1
    lvl_11_14_col_point_bottom_J = lvl_11_14_col.low_flange_main_point_2

#   get main point for top flange
    lvl_11_14_col_point_top_I = lvl_11_14_col.top_flange_main_point_1
    lvl_11_14_col_point_top_J = lvl_11_14_col.top_flange_main_point_2
         
#   get main point for left web
    lvl_11_14_col_point_web_left_I = lvl_11_14_col.web_main_left_point_1
    lvl_11_14_col_point_web_left_J = lvl_11_14_col.web_main_left_point_2 
    
#   get main point for right web
    lvl_11_14_col_point_web_right_I = lvl_11_14_col.web_main_right_point_1
    lvl_11_14_col_point_web_right_J = lvl_11_14_col.web_main_right_point_2            
             
#   opensees section:   
    ops.section('Fiber', 3, '-torsion', 1)
    
    ops.patch("rect" , 1 , 5 , 1 , *lvl_11_14_col_point_bottom_I ,
              *lvl_11_14_col_point_bottom_J)
    ops.patch("rect" , 1 , 5 , 1 , *lvl_11_14_col_point_top_I , 
              *lvl_11_14_col_point_top_J)
    ops.patch("rect" , 1 , 1 , 5 , *lvl_11_14_col_point_web_left_I , 
              *lvl_11_14_col_point_web_left_J)
    ops.patch("rect" , 1 , 1 , 5 , *lvl_11_14_col_point_web_right_I , 
              *lvl_11_14_col_point_web_right_J)
        
    print("\n11-14层柱截面创建完毕")     

# =============================================================================
# create section for beams from all level    
# =============================================================================

#   patch('rect', matTag, numSubdivY, numSubdivZ, *crdsI, *crdsJ)
#   section('Fiber', secTag, '-torsion', torsionMatTag)  

#    International unit: mm
    
    lvl_all_beam = section.HSection(500, 500, 300, 12, 12, 24)
    lvl_all_beam.plot()
    
    col_area_all_beam = lvl_all_beam.compute_area()
    
#   get main point for bottom flange
    lvl_all_beam_point_bottom_I = lvl_all_beam.low_flange_main_point_1
    lvl_all_beam_point_bottom_J = lvl_all_beam.low_flange_main_point_2
    
#   get main point for top flange
    lvl_all_beam_point_top_I = lvl_all_beam.top_flange_main_point_1
    lvl_all_beam_point_top_J = lvl_all_beam.top_flange_main_point_2
         
#   get main point for web
    lvl_all_beam_point_web_I = lvl_all_beam.web_main_point_1
    lvl_all_beam_point_web_J = lvl_all_beam.web_main_point_2             
             
#   opensees section:   
    ops.section('Fiber', 4, '-torsion', 2)
    
    ops.patch("rect" , 2 , 5 , 1 , *lvl_all_beam_point_bottom_I ,
              *lvl_all_beam_point_bottom_J)
    ops.patch("rect" , 2 , 5 , 1 , *lvl_all_beam_point_top_I , 
              *lvl_all_beam_point_top_J)
    ops.patch("rect" , 2 , 1 , 5 , *lvl_all_beam_point_web_I , 
              *lvl_all_beam_point_web_J)
#   section('Aggregator', secTag, *mats, '-section', sectionTag)

    print("\n01-14层梁截面创建完毕")

# =============================================================================
# create geometric-transformation
# =============================================================================

#   geomTransf('PDelta', transfTag, *vecxz, '-jntOffset', *dI, *dJ)    
    # Transf beamL and beamB
    ops.geomTransf("PDelta",  1 ,*[0,0,1] )
    # Transf columns
    ops.geomTransf("PDelta",  2 ,*[1,0,0] )

    print("\n已创建局部坐标系下的定位向量")
# =============================================================================
# create Gauss-Legendre integration points alone the element
# =============================================================================

#    beamIntegration('Legendre', tag, secTag, N)
    
#   Integration for columns from level 01 to 05
    ops.beamIntegration("Legendre", 1 , 1 , 5)

#   Integration for columns from level 06 to 10    
    ops.beamIntegration("Legendre", 2 , 2 , 5)

#   Integration for columns from level 11 to 14    
    ops.beamIntegration("Legendre", 3 , 3 , 5)

#   Integration for beam from L direction  
    ops.beamIntegration("Legendre", 4 , 4 , 5)
            
#   Integration for beam from B direction 
    ops.beamIntegration("Legendre", 5 , 4 , 5)    

    print("\n已创建积分")            
# =============================================================================
# create element for columns
# =============================================================================

#   two kind of element:

#   element('dispBeamColumn', eleTag, *eleNodes, transfTag, integrationTag, 
#          '-cMass', '-mass', mass=0.0)
    
#   element('elasticBeamColumn', eleTag, *eleNodes, Area, E_mod, G_mod, 
#          Jxx, Iy, Iz, transfTag[, '-mass', massPerLength][, '-cMass'])
     
#   Density of steel: 7.85g/cm3
#   Unit conversion: 7.85g/100mm^3 = 0.00000785
    
    unit_mass_Q235B = 7.85*10**(-9) # t/mm^3
    unit_mass_HT590 = 7.35*10**(-9) # t/mm^3

    fig_2 = plt.figure(figsize=(10,10))
    none = Axes3D(fig_2) 
    
#   create element for colunms_lvl_01_05    
    split_num_col_01_05 = 5 
    mass_col_01_05 = col_area_01_05*unit_mass_HT590 
    
    for i in range(0,5):       
        for j in frame_lvl_14.to_columns_nth(i):
            
            col = stu.member_manager.get_object_by_id(j[0])
            col.split(split_num_col_01_05)
            col_split_point = stu.member_manager.get_attribute_by_id(j[0])['split'] 
#            print(col_split_point)
            
            for node_id in range(1 , len(col_split_point)-1):
                ops.node(col_split_point[node_id] , 
                         *stu.node_manager.anti_get(col_split_point[node_id]))
            
            for k in range(len(col_split_point)-1):
                c = stu.Column(none , stu.node_manager.anti_get(col_split_point[k]) , 
                               stu.node_manager.anti_get(col_split_point[k+1]))
                ops.element("dispBeamColumn", c.name , col_split_point[k] , 
                            col_split_point[k+1] , 2 , 1 , '-mass' , mass_col_01_05)

#   when Undivided            
#            ops.element("dispBeamColumn", *j , 2 , 1 , '-mass' , mass)
            
#   create element for colunms_lvl_06_10 
    split_num_06_10 = 5
    mass_col_06_10 = col_area_06_10*unit_mass_HT590 
    
    for i in range(5,10):        
        for j in frame_lvl_14.to_columns_nth(i):
            
            col = stu.member_manager.get_object_by_id(j[0])
            col.split(split_num_06_10)
            col_split_point = stu.member_manager.get_attribute_by_id(j[0])['split'] 
#            print(col_split_point)
            
            for node_id in range(1 , len(col_split_point)-1):
                ops.node(col_split_point[node_id] , 
                         *stu.node_manager.anti_get(col_split_point[node_id]))
            
            for k in range(len(col_split_point)-1):
                c = stu.Column(none , stu.node_manager.anti_get(col_split_point[k]) , 
                               stu.node_manager.anti_get(col_split_point[k+1]))
                ops.element("dispBeamColumn", c.name , col_split_point[k] , 
                            col_split_point[k+1] , 2 , 2 , '-mass' , mass_col_06_10)

#   when Undivided                
#            ops.element("dispBeamColumn", *j , 2 , 2 , '-mass' , mass)

#   create element for colunms_lvl_10_14    
    split_num_10_14 = 5
    mass_col_11_14 = col_area_11_14*unit_mass_HT590
    
    for i in range(10,14):       
        for j in frame_lvl_14.to_columns_nth(i):
            
            col = stu.member_manager.get_object_by_id(j[0])
            col.split(split_num_10_14)
            col_split_point = stu.member_manager.get_attribute_by_id(j[0])['split'] 
#            print(col_split_point)
            
            for node_id in range(1 , len(col_split_point)-1):
                ops.node(col_split_point[node_id] , 
                         *stu.node_manager.anti_get(col_split_point[node_id]))
            
            for k in range(len(col_split_point)-1):
                c = stu.Column(none , stu.node_manager.anti_get(col_split_point[k]) , 
                               stu.node_manager.anti_get(col_split_point[k+1]))
                ops.element("dispBeamColumn", c.name , col_split_point[k] , 
                            col_split_point[k+1] , 2 , 3 , '-mass' , mass_col_11_14)

#   when Undivided                
#            ops.element("dispBeamColumn", *j , 2 , 3 , '-mass' , mass)

# =============================================================================
# create pattern
# =============================================================================
    
    factor = 1.0
    ops.timeSeries('Linear', 1)
    ops.pattern("Plain" , 1 , 1)
    
# =============================================================================
# create element and load for beams
# =============================================================================

#   Unit conversion:
#   1kN/m^2 = 1*1000N/(1000mm*1000mm) = 0.001N/mm^2

#   create element for beamL_lvl_all
    split_num_beam_L = 5
    mass_col_all_beamL = col_area_all_beam*unit_mass_Q235B + 15.0/9800
    
    Wy_L , Wz_L , Wx_L = 0.0 , -mass_col_all_beamL*9800 , 0.0
    
    for i in range(14):        
        for j in frame_lvl_14.to_beamL_nth(i):

            col = stu.member_manager.get_object_by_id(j[0])
            col.splitL(split_num_beam_L)
            col_split_point = stu.member_manager.get_attribute_by_id(j[0])['split'] 
#            print(col_split_point)
            
            for node_id in range(1 , len(col_split_point)-1):
                ops.node(col_split_point[node_id] , 
                         *stu.node_manager.anti_get(col_split_point[node_id]))
            
            for k in range(len(col_split_point)-1):
                c = stu.Column(none , stu.node_manager.anti_get(col_split_point[k]) , 
                               stu.node_manager.anti_get(col_split_point[k+1]))
                
#   element('dispBeamColumn', eleTag, *eleNodes, transfTag, integrationTag, 
#          '-cMass', '-mass', mass=0.0)
                ops.element("dispBeamColumn", c.name , col_split_point[k] , 
                            col_split_point[k+1] , 1 , 4 , '-mass' , mass_col_all_beamL)                

#   eleLoad('-ele', *eleTags, '-range', eleTag1, eleTag2, '-type', '-beamUniform', 
#        Wy, Wz=0.0, Wx=0.0, '-beamPoint', Py, Pz=0.0, xL, Px=0.0, '-beamThermal', *tempPts)
                
#   create load for beamL_lvl_all:               
                ops.eleLoad("ele" , c.name , "-range" , c.name , c.name , 
                            '-type' , '-beamUniform' , Wy_L , Wz_L , Wx_L)
                
#   when Undivided                
#            ops.element("dispBeamColumn", *j , 1 , 4 , '-mass' , mass)
            
#   create element for beamB_lvl_all
    split_num_beam_B = 5
    mass_col_all_beamB = col_area_all_beam*unit_mass_Q235B + 15.0/9800
            
    Wy_B , Wz_B , Wx_B = 0.0 , -mass_col_all_beamB*9800 ,  0.0
    
    for i in range(14):
        for j in frame_lvl_14.to_beamB_nth(i):

            col = stu.member_manager.get_object_by_id(j[0])
            col.splitB(split_num_beam_B)
            col_split_point = stu.member_manager.get_attribute_by_id(j[0])['split'] 
#            print(col_split_point)
            
            for node_id in range(1 , len(col_split_point)-1):
                ops.node(col_split_point[node_id] , 
                         *stu.node_manager.anti_get(col_split_point[node_id]))
            
            for k in range(len(col_split_point)-1):
                c = stu.Column(none , stu.node_manager.anti_get(col_split_point[k]) , 
                               stu.node_manager.anti_get(col_split_point[k+1]))
                
#   element('dispBeamColumn', eleTag, *eleNodes, transfTag, integrationTag, 
#          '-cMass', '-mass', mass=0.0)
                ops.element("dispBeamColumn", c.name , col_split_point[k] , 
                            col_split_point[k+1] , 1 , 5 , '-mass' , mass_col_all_beamB)

#   eleLoad('-ele', *eleTags, '-range', eleTag1, eleTag2, '-type', '-beamUniform', 
#        Wy, Wz=0.0, Wx=0.0, '-beamPoint', Py, Pz=0.0, xL, Px=0.0, '-beamThermal', *tempPts)

#   create load for beamB_lvl_all                 
                ops.eleLoad("ele" , c.name , "-range" , c.name , c.name , 
                            '-type' , '-beamUniform' , Wy_B , Wz_B , Wx_B)
                
#   when Undivided                
#            ops.element("dispBeamColumn", *j , 1 , 5 , '-mass' , mass)
 
    print("\n已创建单元体") 
#    opsplt.plot_model()    

# =============================================================================
# creat damper support(a) for level 01:
# =============================================================================
 
    level_01_damper_support_a = []
    
#   the first damper support:
    
    damper_support_point_lvl_01_1 = frame_lvl_14.columns[0][1][0].point1   
    damper_support_point_lvl_01_2 = frame_lvl_14.columns[0][2][0].point2

    direction_vector_1 = (np.array(damper_support_point_lvl_01_2) - 
                          np.array(damper_support_point_lvl_01_1))
    print("\nLevel01层支撑的第一方向向量为："+ str(direction_vector_1))
    
    damper_support_1 = stu.Column(stu.axe , damper_support_point_lvl_01_1 , 
                                  damper_support_point_lvl_01_2)
    
    level_01_damper_support_a.append(damper_support_1)    
  
#   the secound damper support:
    
    damper_support_point_lvl_01_3 = frame_lvl_14.columns[0][1][3].point1
    damper_support_point_lvl_01_4 = frame_lvl_14.columns[0][2][3].point2
    
    damper_support_2 = stu.Column(stu.axe , damper_support_point_lvl_01_3 , 
                                  damper_support_point_lvl_01_4)
    
    level_01_damper_support_a.append(damper_support_2)    
    
#   the thrid damper support:
    
    damper_support_point_lvl_01_5 = frame_lvl_14.columns[0][1][6].point1
    damper_support_point_lvl_01_6 = frame_lvl_14.columns[0][2][6].point2
    
    damper_support_3 = stu.Column(stu.axe , damper_support_point_lvl_01_5 , 
                                  damper_support_point_lvl_01_6)
    
    level_01_damper_support_a.append(damper_support_3)     
   
#    print(level_01_damper_support_a)
    
# =============================================================================
# creat damper support(b) for level 01:
# =============================================================================
 
    level_01_damper_support_b = []
    
#   the first damper support:
    
    damper_support_point_lvl_01_7 = frame_lvl_14.columns[0][1][0].point2   
    damper_support_point_lvl_01_8 = frame_lvl_14.columns[0][2][0].point1

    direction_vector_2 = (np.array(damper_support_point_lvl_01_8) - 
                          np.array(damper_support_point_lvl_01_7))
    print("\nLevel01层支撑的第二方向向量为："+ str(direction_vector_2))
    
    damper_support_4 = stu.Column(stu.axe , damper_support_point_lvl_01_7 , 
                                  damper_support_point_lvl_01_8)
    
    level_01_damper_support_b.append(damper_support_4)    
  
#   the secound damper support:
    
    damper_support_point_lvl_01_9 = frame_lvl_14.columns[0][1][3].point2
    damper_support_point_lvl_01_10 = frame_lvl_14.columns[0][2][3].point1
    
    damper_support_5 = stu.Column(stu.axe , damper_support_point_lvl_01_9 , 
                                  damper_support_point_lvl_01_10)
    
    level_01_damper_support_b.append(damper_support_5)    
    
#   the thrid damper support:
    
    damper_support_point_lvl_01_11 = frame_lvl_14.columns[0][1][6].point2
    damper_support_point_lvl_01_12 = frame_lvl_14.columns[0][2][6].point1
    
    damper_support_6 = stu.Column(stu.axe , damper_support_point_lvl_01_11 , 
                                  damper_support_point_lvl_01_12)
    
    level_01_damper_support_b.append(damper_support_6)     
   
#    print(level_01_damper_support_b)
    
    level_01_damper_support = []
    level_01_damper_support.append(level_01_damper_support_a)
    level_01_damper_support.append(level_01_damper_support_b)
#    print(level_01_damper_support)
    
    print("\n01层支撑位置信息创建完毕")
    
# =============================================================================
# creat damper support for level 02 ~ level 05:
# =============================================================================
    
    direction_vector_3 = (np.array(frame_lvl_14.columns[1][1][0].point1) - 
                          np.array(frame_lvl_14.columns[1][2][0].point2))
    print("\nLevel02~14层支撑的第一方向向量为："+ str(direction_vector_3))
    
    direction_vector_4 = (np.array(frame_lvl_14.columns[1][1][0].point2) - 
                          np.array(frame_lvl_14.columns[1][2][0].point1))
    print("\nLevel02~14层支撑的第二方向向量为："+ str(direction_vector_4))
    
    level_02_05_damper_support_a , level_02_05_damper_support_b = [] , []
    
    for i in range(1 , 5):
        damper_support_point_lvl_02_14_1a = frame_lvl_14.columns[i][1][0].point1
        damper_support_point_lvl_02_14_2a = frame_lvl_14.columns[i][2][0].point2
        damper_support_a = stu.Column(stu.axe , damper_support_point_lvl_02_14_1a , 
                                      damper_support_point_lvl_02_14_2a)
        
        level_02_05_damper_support_a.append(damper_support_a)
        
        damper_support_point_lvl_02_14_1b = frame_lvl_14.columns[i][1][0].point2
        damper_support_point_lvl_02_14_2b = frame_lvl_14.columns[i][2][0].point1
        damper_support_b = stu.Column(stu.axe , damper_support_point_lvl_02_14_1b , 
                                      damper_support_point_lvl_02_14_2b)
        
        level_02_05_damper_support_b.append(damper_support_b)                
        
        damper_support_point_lvl_02_14_3a = frame_lvl_14.columns[i][1][3].point1
        damper_support_point_lvl_02_14_4a = frame_lvl_14.columns[i][2][3].point2
        damper_support_c = stu.Column(stu.axe , damper_support_point_lvl_02_14_3a , 
                                      damper_support_point_lvl_02_14_4a)
        
        level_02_05_damper_support_a.append(damper_support_c)
        
        damper_support_point_lvl_02_14_3b = frame_lvl_14.columns[i][1][3].point2
        damper_support_point_lvl_02_14_4b = frame_lvl_14.columns[i][2][3].point1
        damper_support_d = stu.Column(stu.axe , damper_support_point_lvl_02_14_3b , 
                                      damper_support_point_lvl_02_14_4b)
        
        level_02_05_damper_support_b.append(damper_support_d)
        
        damper_support_point_lvl_02_14_5a = frame_lvl_14.columns[i][1][6].point1
        damper_support_point_lvl_02_14_6a = frame_lvl_14.columns[i][2][6].point2
        damper_support_e = stu.Column(stu.axe , damper_support_point_lvl_02_14_5a , 
                                      damper_support_point_lvl_02_14_6a)
        
        level_02_05_damper_support_a.append(damper_support_e)
        
        damper_support_point_lvl_02_14_5b = frame_lvl_14.columns[i][1][6].point2
        damper_support_point_lvl_02_14_6b = frame_lvl_14.columns[i][2][6].point1
        damper_support_f = stu.Column(stu.axe , damper_support_point_lvl_02_14_5b , 
                                      damper_support_point_lvl_02_14_6b)
        
        level_02_05_damper_support_b.append(damper_support_f)        

    level_02_05_damper_support = []
    level_02_05_damper_support.append(level_02_05_damper_support_a)
    level_02_05_damper_support.append(level_02_05_damper_support_b)
#    print(len(level_02_14_damper_support[0]) , len(level_02_14_damper_support[1]))

    print("\n02~05支撑位置信息创建完毕")

# =============================================================================
# creat damper support for level 06 ~ level 14:
# =============================================================================
    
    level_06_14_damper_support_a , level_06_14_damper_support_b = [] , []
    
    for i in range(5 , 14):
        damper_support_point_lvl_02_14_1a = frame_lvl_14.columns[i][1][0].point1
        damper_support_point_lvl_02_14_2a = frame_lvl_14.columns[i][2][0].point2
        damper_support_a = stu.Column(stu.axe , damper_support_point_lvl_02_14_1a , 
                                      damper_support_point_lvl_02_14_2a)
        
        level_06_14_damper_support_a.append(damper_support_a)
        
        damper_support_point_lvl_02_14_1b = frame_lvl_14.columns[i][1][0].point2
        damper_support_point_lvl_02_14_2b = frame_lvl_14.columns[i][2][0].point1
        damper_support_b = stu.Column(stu.axe , damper_support_point_lvl_02_14_1b , 
                                      damper_support_point_lvl_02_14_2b)
        
        level_06_14_damper_support_b.append(damper_support_b)                
        
        damper_support_point_lvl_02_14_3a = frame_lvl_14.columns[i][1][3].point1
        damper_support_point_lvl_02_14_4a = frame_lvl_14.columns[i][2][3].point2
        damper_support_c = stu.Column(stu.axe , damper_support_point_lvl_02_14_3a , 
                                      damper_support_point_lvl_02_14_4a)
       
        level_06_14_damper_support_a.append(damper_support_c)
        
        damper_support_point_lvl_02_14_3b = frame_lvl_14.columns[i][1][3].point2
        damper_support_point_lvl_02_14_4b = frame_lvl_14.columns[i][2][3].point1
        damper_support_d = stu.Column(stu.axe , damper_support_point_lvl_02_14_3b , 
                                      damper_support_point_lvl_02_14_4b)
        
        level_06_14_damper_support_b.append(damper_support_d)
        
        damper_support_point_lvl_02_14_5a = frame_lvl_14.columns[i][1][6].point1
        damper_support_point_lvl_02_14_6a = frame_lvl_14.columns[i][2][6].point2
        damper_support_e = stu.Column(stu.axe , damper_support_point_lvl_02_14_5a , 
                                      damper_support_point_lvl_02_14_6a)
        
        level_06_14_damper_support_a.append(damper_support_e)
        
        damper_support_point_lvl_02_14_5b = frame_lvl_14.columns[i][1][6].point2
        damper_support_point_lvl_02_14_6b = frame_lvl_14.columns[i][2][6].point1
        damper_support_f = stu.Column(stu.axe , damper_support_point_lvl_02_14_5b , 
                                      damper_support_point_lvl_02_14_6b)
        
        level_06_14_damper_support_b.append(damper_support_f)        

    level_06_14_damper_support = []
    level_06_14_damper_support.append(level_06_14_damper_support_a)
    level_06_14_damper_support.append(level_06_14_damper_support_b)
#    print(len(level_02_14_damper_support[0]) , len(level_02_14_damper_support[1])

    print("\n05~14支撑位置信息创建完毕")
        
# =============================================================================
# creat damper support material for level all:    
# =============================================================================
  
#   LY100:
    Fy_c = 100.0	        # STEEL yield stress
    Es_c = 2.06*10**5	    # modulus of steel
    Bs_c = 0.01		        # strain-hardening ratio 
    R0_c = 18.0		        # control the transition from elastic to plastic branches
    cR1_c = 0.925	        # control the transition from elastic to plastic branches
    cR2_c = 0.15		    # control the transition from elastic to plastic branches
#    uniaxialMaterial('Steel02', matTag, Fy, E0, b, *params, a1=a2*Fy/E0, 
#                       a2=1.0, a3=a4*Fy/E0, a4=1.0, sigInit=0.0)

    ops.uniaxialMaterial('Steel02', 3 , Fy_c, Es_c, Bs_c, R0_c , cR1_c , cR2_c)
    
    print("\n已创建支撑材料")

# =============================================================================
# Necessary parameters for damper support
# =============================================================================
   
#   unit: mm^2
    section_area_lvl_01_05 = 22400
    section_area_lvl_06_14 = 13200   
    
    unit_mass_LY100 = 7.35*10**(-9)
    
    damper_support_mass_lvl_01_05 = section_area_lvl_01_05*unit_mass_LY100
    damper_support_mass_lvl_06_14 = section_area_lvl_06_14*unit_mass_LY100
    
# =============================================================================
# creat damper support in opensees:   
# =============================================================================

#   element('Truss', eleTag, *eleNodes, A, matTag
#           [, '-rho', rho][, '-cMass', cFlag][, '-doRayleigh', rFlag]) 

#   create level 01 damper support in ops:    
    for i in level_01_damper_support[0]:
        ops.element("Truss" , i.name , *[stu.node_manager.get(i.point1) , 
                                         stu.node_manager.get(i.point2)] , 
                    section_area_lvl_01_05 , 3 , "-rho" , damper_support_mass_lvl_01_05)
    
    for i in level_01_damper_support[1]:
        ops.element("Truss" , i.name , *[stu.node_manager.get(i.point1) , 
                                         stu.node_manager.get(i.point2)] , 
                    section_area_lvl_01_05 , 3 , "-rho" , damper_support_mass_lvl_01_05)
    
#   create level 02 ~ level 05 damper support in ops:     
    for i in level_02_05_damper_support[0]:
        ops.element("Truss" , i.name , *[stu.node_manager.get(i.point1) , 
                                         stu.node_manager.get(i.point2)] , 
                    section_area_lvl_01_05 , 3 , "-rho" , damper_support_mass_lvl_01_05)
    
    for i in level_02_05_damper_support[1]:
        ops.element("Truss" , i.name , *[stu.node_manager.get(i.point1) , 
                                         stu.node_manager.get(i.point2)] , 
                    section_area_lvl_01_05 , 3 , "-rho" , damper_support_mass_lvl_01_05)
    
#   create level 02 ~ level 05 damper support in ops:     
    for i in level_06_14_damper_support[0]:
        ops.element("Truss" , i.name , *[stu.node_manager.get(i.point1) , 
                                         stu.node_manager.get(i.point2)] , 
                    section_area_lvl_01_05 , 3 , "-rho" , damper_support_mass_lvl_06_14)
    
    for i in level_06_14_damper_support[1]:
        ops.element("Truss" , i.name , *[stu.node_manager.get(i.point1) , 
                                         stu.node_manager.get(i.point2)] , 
                    section_area_lvl_01_05 , 3 , "-rho" , damper_support_mass_lvl_06_14)

    print("\n支撑创建完毕")
    
#   D.va draw    
    frame_lvl_14.plot()
    
#   official draw    
    opsplt.plot_model()   
    
# =============================================================================
# create fix
# =============================================================================

    nodes_lvl_00 = frame_lvl_14.to_columns_nth(0)
#    print(frame_lvl_14.to_columns_nth(0))
#    
##    fix(nodeTag, *constrValues)
    fully_fixed = [1 , 1 , 1 , 1 , 1 , 1]
    
    for i in nodes_lvl_00:
#        foundation = stu.node_manager.anti_get(i[1])
#        print(i[1])
#        print(foundation)
        ops.fix(i[1] , *fully_fixed)
#    ops.fix(nodes_lvl_00[1][1]  , *fully_fixed)   
    
#   fixZ(z, *constrValues, '-tol', tol=1e-10)
#    ops.fixZ(0.0 , *fully_fixed)

    print("\n已创建约束")
      
# =============================================================================
# create pattern
# =============================================================================
#    pattern('Plain', patternTag, tsTag, '-fact', fact)
#    
#    factor = 1.0
#    ops.timeSeries('Linear', 1)
#    ops.pattern("Plain" , 1 , 1)
#    
# =============================================================================
# create load (when not split)   
# =============================================================================
#eleLoad('-ele', *eleTags, '-range', eleTag1, eleTag2, '-type', 
#        '-beamUniform', Wy, Wz=0.0, Wx=0.0, '-beamPoint', Py, Pz=0.0, xL, 
#        Px=0.0, '-beamThermal', *tempPts)
    
##    createBeamL load 
#    
#    Wx_B , Wy_B , Wz_B = 0.0 , 0.0 , -18.5*1000
#    for i in range(14):
#        for j in frame_lvl_14.to_beamB_nth(i):
##            print(j)
#            ops.eleLoad("ele" , j[0] , '-type' , '-beamUniform' , Wx_B , Wy_B , Wz_B)
#            
#    Wx_L , Wy_L , Wz_L = 0.0 , 0.0 , -15*1000    
#    for i in range(14):
#        for j in frame_lvl_14.to_beamL_nth(i):
#            ops.eleLoad("ele" , j[0] , '-type' , '-beamUniform' , Wx_L , Wy_L , Wz_L)
##    print(frame_lvl_14.to_columns_nth(13)) 
#      
#    print("\n已创建荷载") 
#    
# =============================================================================
# creat constraint between nodes   
# =============================================================================
#   rigidDiaphragm(perpDirn, rNodeTag, *cNodeTags)
    
    node_lvl_nth = []
    retained_node_group = []
    for i in range(14):
        retained_node = frame_lvl_14.to_columns_nth(i)[0][2] 
        retained_node_group.append(retained_node)
        for node in frame_lvl_14.to_columns_nth(i):
            node_lvl_nth.append(node[2])
            
#        ops.rigidDiaphragm(3 , retained_node , *node_lvl_nth)
        node_lvl_nth.clear()
        
    print("\n每层的主节点为：")
    print(retained_node_group)  
    
# =============================================================================
# create record
# =============================================================================

#recorder('Node', '-file', filename, '-xml', filename, '-binary', filename, 
#         '-tcp', inetAddress, port, '-precision', nSD=6, '-timeSeries', 
#          tsTag, '-time', '-dT', deltaT=0.0, '-closeOnWrite', 
#         '-node', *nodeTags=[], '-nodeRange', startNode, endNode, 
#         '-region', regionTag, '-dof', *dofs=[], respType)            
    
#recorder('EnvelopeNode', '-file', filename, '-xml', filename, '-precision', 
#         nSD=6, '-timeSeries', tsTag, '-time', '-dT', deltaT=0.0, 
#         '-closeOnWrite', '-node', *nodeTags=[], '-nodeRange', 
#         startNode, endNode, '-region', regionTag, '-dof', *dofs=[], respType)
     
    filename_1 = "disp_x.txt"
    ops.recorder("Node" , "-file" , filename_1 , "time" , "-node" , 
                 *retained_node_group  , "-dof" , 1 , "disp")
    
    filename_1 = "resisting_force.txt"
    
    nodes_lvl_00 = frame_lvl_14.to_columns_nth(0)
    resisting_force_group = []
    for i in nodes_lvl_00:
        resisting_force_group.append(i[1])
#    print(resisting_force_group)
    
#    for i in resisting_force_group:
#        print(stu.node_manager.anti_get(i))
    
    ops.recorder("Node" ,"-file" , filename_1 , "time" , "-node" ,  
                 *resisting_force_group  , "-dof" , 3 , "reaction")
    
    print("\n已创建记录器")
# =============================================================================
# 
# =============================================================================
    
    ops.constraints('Transformation')
    print("\n constraints完成")
    
    ops.numberer('RCM')
    print("\n numberer完成")
    
#    ops.system('SparseSYM') 
    ops.system('SparseGeneral')
    print("\n system完成")

# =============================================================================
# for test
# =============================================================================

#    test('NormDispIncr', tol, iter, pFlag=0, nType=2)
    ops.test("NormDispIncr", 0.1 , 2000 , 2)
    print("\n test完成")

# =============================================================================
# 
# =============================================================================
    
    ops.algorithm("NewtonLineSearch" , False , False , False , False , 0.75)
#    ops.algorithm('Newton')
    print("\n algorithm完成")
    
#    integrator('LoadControl', incr, numIter=1, minIncr=incr, maxIncr=incr)
    ops.integrator("LoadControl" , 0.1)
    print("\n integrator完成")
    
    ops.analysis("Static")
    print("\n analysis完成")
    
#    opsplt.plot_model()
    
# =============================================================================
# 
# =============================================================================
    
#    filename_1 = "resisting_force.txt"
#    
#    nodes_lvl_00 = frame_lvl_14.to_columns_nth(0)
#    resisting_force_group = []
#    for i in nodes_lvl_00:
#        resisting_force_group.append(i[1])
##    print(resisting_force_group)
#    
##    for i in resisting_force_group:
##        print(stu.node_manager.anti_get(i))
#    
#    ops.recorder("Node" ,"-file" , filename_1 , "time" , "-node" ,  
#                 *resisting_force_group  , "-dof" , 3 , "reaction")
    
# =============================================================================
# caculate eigen and cycle time
# =============================================================================

#    num_Modes = 10
##    eigen(solver='-genBandArpack', numEigenvalues)
#    eigen_value = ops.eigen("-genBandArpack" , num_Modes)
#    print("特征值为：" + str(eigen_value))
#    
#    import math as math
#    pi = math.pi
#    cycle_T = []
#    for eigen in eigen_value:
#        cycle_T.append(2*pi/pow(eigen , 0.5))
#    print("周期为：" + str(cycle_T))    
##  T = (0.08~0.12)N =(0.08~0.12)*14 = (1.12 ~ 1.68)s    
#    print("经验公式周期为：(1.12 ~ 1.68)s")
# =============================================================================
# 
# =============================================================================

    ops.analyze(10)
    print("\n analyze完成")
        
    ops.loadConst('-time', 0.0)

    print("\n重力荷载分析完成")
    
    opsplt.plot_model()   
# =============================================================================
# create rayleigh damping
# =============================================================================
    xDamp = 0.02   
    MpropSwitch = 1.0    
    KcurrSwitch = 1.0
    
    KcommSwitch = 0.0
    KinitSwitch = 0.0

    lambdaI = 3.8846291886219655
    lambdaJ = 64.78437186628662
    omegaI = pow(lambdaI , 0.5)
    omegaJ = pow(lambdaJ , 0.5)
    
    alphaM = MpropSwitch*xDamp*(2*omegaI*omegaJ)/(omegaI + omegaJ)
    betaKcurr = KcurrSwitch*2*xDamp/(omegaI+omegaJ)
    betaKcomm = KcommSwitch*2*xDamp/(omegaI+omegaJ)
    betaKinit = KinitSwitch*2*xDamp/(omegaI+omegaJ)
    
    ops.rayleigh(alphaM, betaKcurr , betaKinit, betaKcomm)
    
    print("\n已创建rayleigh")
# =============================================================================
# clear all Analysis object    
# =============================================================================
    ops.wipeAnalysis()
# =============================================================================
# create timeSeries 
# =============================================================================
    
    IDloadTag = 1001
    iGMfile = pd.read_csv("GMX.txt" , header = None)
    iGMdirection = 1
    iGMfact = "210*10"
    dt = 0.01
    GMfatt = 2101
    
#timeSeries('Path', tag, '-dt', dt=0.0, '-values', *values, '-time', *time, 
#           '-filepath', filepath='', '-fileTime', fileTime='', 
#           '-factor', factor=1.0, '-startTime', startTime=0.0, '-useLast', '-prependZero')
    filepath_01 = "GMX.txt"   
    ops.timeSeries('Path', 2 , '-dt', dt , '-filePath', filepath_01 , '-factor', GMfatt) 
    
    print("\n已创建时间序")
# =============================================================================
# create pattern
# =============================================================================
#    pattern('UniformExcitation', patternTag, dir, '-disp', dispSeriesTag, 
#            '-vel', velSeriesTag, '-accel', accelSeriesTag, '-vel0', vel0, '-fact', fact)   

#    pattern UniformExcitation $IDloadTag $iGMdirection -accel $AccelSeries;
    ops.pattern("UniformExcitation" , IDloadTag , iGMdirection , "-accel" , 2)
    
# =============================================================================
# create constraints
# =============================================================================
    ops.constraints('Transformation')
# =============================================================================
# create number
# =============================================================================
    ops.numberer('RCM')
# =============================================================================
# cteate system    
# =============================================================================
    ops.system('SparseSYM')    
# =============================================================================
# create test    
# =============================================================================  
#    test('NormDispIncr', tol, iter, pFlag=0, nType=2)
    test_num_max = 1*10**(-3)
    ops.test('NormDispIncr', test_num_max , 10 , 2)
#    test NormDispIncr 1e-3 10 2
    
# =============================================================================
# create algorithm    
# =============================================================================
    
#    algorithm('NewtonLineSearch', Bisection=False, Secant=False, 
#               RegulaFalsi=False, InitialInterpolated=False, tol=0.8, 
#               maxIter=10, minEta=0.1, maxEta=10.0)
    ops.algorithm("NewtonLineSearch" , False , False , False , False , 0.75)
    
# =============================================================================
# create integrator   
# =============================================================================
#    integrator('Newmark', gamma, beta, '-formD', form)
    
    ops.integrator("Newmark" ,  0.5 , 0.25)
# =============================================================================
# create analysis
# =============================================================================
    ops.analysis('Transient')
# =============================================================================
# create analyze  
# =============================================================================
#    analyze(numIncr=1, dt=0.0, dtMin=0.0, dtMax=0.0, Jd=0)
    
    ops.analyze(2000 , 0.01) 
    print("\n分析完成")
# =============================================================================
# Clear Memory    
# =============================================================================
    ops.wipe()
    print("\n已清空OPENSEES内存")
    
    del stu.node_manager
    print("\n已经清空节点管理器")
    
    del stu.member_manager
    print("\n已经清空单元对象管理器")
    
    stu.GLOBAL_NAME = 0
    print("\n已经重置计数器")
# =============================================================================
# End   
# ============================================================================= 
    

    
    
    
    
    
    
    
    
    
    
    