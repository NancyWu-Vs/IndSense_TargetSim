import femm
import matplotlib.pyplot as plt
import numpy as np
import os
import CSVWriter


def main():

    femm.openfemm() # Starts the FEMM software. FEMM must be installed for this to be operational
    template = "TargetSim.FEM" #File that contains the coil geometry
    pth= os.getcwd(); 

    #default values
    maxwidth = 3
    minwidth = 0.001
    inc = 1
    radoffset = 0
    axoffset = 0
    target = 2
    background = 0
    backer = 2
    targety1base = 4.85
    targetthickness = 0.025
    
    pL = [] # inductance of the positive coil
    nL = [] # inductance of the negative coil
    targsize = []
    Materials = ["Air", "Copper", "EFW","316 Stainless Steel","416 Stainless Steel", "Mu Metal", "17-4"]
    
    try:
        femm.opendocument(pth+'\\'+template) #Assuming the template file is placed in the same folder as this file
    except Exception as e:
        print("Template not found" + str(e))

    confirm = 'n'
    print("The current document you are working off of is: " + template)

    #Asks user for what params they want to change and saves it in a list by number
    while(not(confirm == 'y' or confirm == 'Y')):
        params = input("""Please list all parameters you would like to edit by number separated by a comma(e.g. 1,3,5) or 0 for default settings
                   1. Max Width (Default 3mm)
                   2. Min Width (Default 0.001mm)
                   3. Increment (Default 0.2mm - expands outwards 0.1mm each iteration)
                   4. Radial/Horizontal Offset (Default Distance 0mm)
                   5. Axial Offset/Distance between Target (Default Distance 0.1mm between)
                   6. Target Material (Default: EFW)
                   7. Background Material (Default: Air)
                   8. Coil Backer Material (Default: EFW)
                   """) or '0'

        try:
            params = params.split(',')
            params =[int(i) for i in params]
            params.sort()
        except Exception as e:
            print('Invalid selection: '+ str(e) + "\n")
            confirm = 'n'
        else:
            print("Your selections are: "+ str(params) +"\n")
            confirm = input("Are you satisfied with your selection? (press y or Y), any other value will have you list the parameters again: \n")
    
    
    #Goes through the list of changing parameters and allows editting
    confirm = 'n' 
    while(not(confirm == 'y' or confirm == 'Y') and not(params[0]==0)):
        for i in params:
            match i:
                case 1:
                    maxwidth = float(input("Please input the max width of target in mm (0.001<x<3.0): \n") or 3.0)
                    while (0.001>maxwidth or maxwidth>3):
                        maxwidth = float(input("Please input the max width of target in mm (0.001<x<3.0): \n") or 3.0)
                    inc = maxwidth/2
                case 2:
                    minwidth = float(input("Please input the min width of target (mm)(0.0<x<max): \n") or 0.001)
                    while(minwidth<0.001 or minwidth>maxwidth):
                        minwidth = float(input("Please input the min width of target (mm)(0.0<x<max): \n") or 0.001)
                case 3:
                    inc = float(input("Please input increment of target (mm): \n") or 0.1) 
                    while(inc>maxwidth):
                        inc = float(input("Please input increment of target (mm): \n") or 0.1) 
                case 4:
                    radoffset = float(input ("Please input the radial offset in mm of target (-/+ 0.5mm): \n") or 0)
                    while(abs(radoffset)>0.5):
                        radoffset = float(input ("Please input the radial offset in mm of target (-/+ 0.5mm): \n") or 0)
                case 5:
                    axoffset = float(input("Please input the axial offset between -0.275mm and 1 (distance between target and coil in mm). Added to the default distance of 0.275 mm (e.g. inputting zero will leave it at 0.275mm): \n") or 0)
                    while(-0.275>axoffset or axoffset>1):
                        axoffset = float(input("Please input the axial offset between -0.275mm and 1 (distance between target and coil in mm). Added to the default distance of 0.275 mm (e.g. inputting zero will leave it at 0.275mm): \n") or 0)
                case 6:
                    target = int(input ("Please input the target material: 0-Air, 1-Copper, 2-EFW, 3-316 Stainless Steel, 4-416 Stainless Steel, 5-mu Metal, 6-17-4: \n" or 2))
                    while(0>target or target > len(Materials)):
                        target = int(input ("Please input the target material: 0-Air, 1-Copper, 2-EFW, 3-316 Stainless Steel, 4-416 Stainless Steel, 5-mu Metal, 6-17-4: \n" or 2))
                case 7:
                    background = int(input("Please put the background (behind target) material: 0-Air, 1-Copper, 2-EFW, 3-316 Stainless Steel, 4-416 Stainless Steel, 5-mu Metal, 6-17-4: \n") or 0)
                    while(0>background or background > len(Materials)):
                        background = int(input("Please put the background (behind target) material: 0-Air, 1-Copper, 2-EFW, 3-316 Stainless Steel, 4-416 Stainless Steel, 5-mu Metal, 6-17-4: \n") or 0)
                case 8:
                    backer = int(input("Please input the backer material (behind coil): 0-Air, 1-Copper, 2-EFW, 3-316 Stainless Steel, 4-416 Stainless Steel, 5-mu Metal, 6-17-4: \n") or 2)
                    while(0>backer or backer > len(Materials)):
                        backer = int(input("Please input the backer material (behind coil): 0-Air, 1-Copper, 2-EFW, 3-316 Stainless Steel, 4-416 Stainless Steel, 5-mu Metal, 6-17-4: \n") or 2)
                case _  :
                    pass
        confirm = input("Are you satisfied with your selection (Press y or Y). Any other key will allow redefinition of parameters: \n")

    center = 7.125 + radoffset;
    nmax = int((maxwidth-minwidth)/(inc*2))
    targety1 = targety1base+axoffset
    targety2 = targety1base+targetthickness+axoffset
    csv = CSVWriter.CSVWriter("IndSense_FEMM_TargetSweep")

    femm.mi_addblocklabel(center,4.575)
    femm.mi_selectlabel(center,4.575)
    femm.mi_setblockprop(Materials[backer], 1, 1, '<None>', 0, 0, 0) #blockname, automesh, meshsize, circuit name, magnitization direction, group, number of turns

    for n in range(0,nmax):
        targetx2 = center+minwidth/2+inc*(n)
        targetx1 = center-(minwidth/2+inc*(n))

        #Clear previous
        femm.mi_selectrectangle(5.125,targety1-0.05,8.625,targety2+0.05,4)
        femm.mi_deleteselected()
        
        #Target
        femm.mi_drawrectangle(targetx1,targety1,targetx2,targety2)
        femm.mi_addblocklabel(center,targety1+targetthickness/2)
        femm.mi_selectlabel(center,targety1+targetthickness/2)
        femm.mi_setblockprop(Materials[target], 1, 1, '<None>', 0, 0, 0)

        femm.mi_drawrectangle(5.625,targety1,targetx1,targety2)
        femm.mi_addblocklabel(5.63,targety1+targetthickness/2)
        femm.mi_selectlabel(5.63,targety1+targetthickness/2)
        femm.mi_setblockprop(Materials[background], 1, 1, '<None>', 0, 0, 0)
        femm.mi_clearselected()
        
        femm.mi_drawrectangle(targetx2,targety1,8.625,targety2)
        femm.mi_addblocklabel(8.62,targety1+targetthickness/2)
        femm.mi_selectlabel(8.62,targety1+targetthickness/2)
        femm.mi_setblockprop(Materials[background], 1, 1, '<None>', 0, 0, 0) 
        femm.mi_clearselected()
        

        femm.mi_zoomnatural()
        femm.mi_saveas(pth+"\Coil_targetsweep_py.fem")

        femm.mi_analyze()
        femm.mi_loadsolution()

        #femm.mo_seteditmode('contour')
        #femm.mo_addcontour(targetx1,targety1)
        #femm.mo_addcontour(targetx2,targety1)
        #femm.mo_makeplot(1,1500)#|B|

        pvals = femm.mo_getcircuitproperties('Coil_Pos')
        pL.append(pvals[2]/pvals[0]*2)
        targsize.append(targetx2-targetx1)
        nvals = femm.mo_getcircuitproperties('Coil_Neg')
        nL.append(nvals[2]/nvals[0]*2)

        

    plt.plot(targsize,np.real(pL))
    plt.ylabel('Inductance, Henries')
    plt.xlabel('Target Width (mm)')
    plt.title('Inductance by '+Materials[target]+' Target Width with '+Materials[backer]+' Backer and '+Materials[background]+' Background, \n'+csv.filename)
    lgd = "FSR: "+ str(round(min(np.absolute((pL))),9)*2) +" to " + str(round(max(np.absolute((pL))),9)*2)
    plt.legend([lgd])
    plt.grid(True)
    plt.xticks(np.arange(min(targsize),max(targsize)+1,inc))
    plt.show()

    print(pL)
    input()

if __name__ == '__main__':
    main()
    print("Finished!")
    
