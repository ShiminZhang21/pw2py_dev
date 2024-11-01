import pw2py as pw
fp = "./4x4x3.vasp" #the pristine 4x4x3 build file
geo = pw.atomgeo.from_file(fp, ftype='vasp')


import numpy as np
help(geo.sort_ions)

#print(geo.ion)

def Arrange_atoms(geo, species_order = ["Zn","O"]):
    #parse the ion and position (in the order providede)
    Ion_pos = []
    for ion, p in zip(geo.ion,geo.pos):
        Ion_pos.append([ion, p])

    #sort key
    def sort_key(item):
        ion, pos = item
        #
        species_index = species_order.index(ion)
        return (species_index, pos[0], pos[1])

    #sort the ion
    Ion_pos_sorted = sorted(Ion_pos, key=sort_key)

    #convert back to geometry
    Ion = []
    POS = []
    for ion,p in Ion_pos_sorted:
        Ion.append(ion)
        POS.append(p)
    geo.ion = np.array(Ion)
    geo.pos = np.array(POS)


def Replace_atom(geo,old_pos,new_atom):
    """
    Replace the atom at crystal coordinate=old_pos into new atom;
    INPUT:
        geo: geometry object load by :
            import pw2py as pw
            pw.atomgeo.from_file(fp, ftype='qeinp')
        old_pos = np.array([x,y,z])
        new_atom = str : atom name
    OUTPUT:
        geometry object; 
    """
    import copy
    new_geo=copy.deepcopy(geo)
    for i, vec in enumerate(new_geo.pos):
        distance =np.linalg.norm(vec-old_pos)
        #print(distance)
        if distance<0.1:
            print("Atom at position{} is {}, index {}".format(old_pos,new_geo.ion[i],i))
            print("replace ion with {}".format(new_atom))
            new_geo.ion[i]=new_atom 
    return new_geo

def Remove_atom(geo, old_pos):
    """
    Remove the atom at crystal coordinate=old_pos;
    INPUT:
        geo: geometry object load by :
            import pw2py as pw
            pw.atomgeo.from_file(fp, ftype='qeinp')
        old_pos = np.array([x,y,z])
    OUTPUT:
        geometry object; 
    """
    import copy
    new_geo=copy.deepcopy(geo)
    for i, vec in enumerate(new_geo.pos):
        distance =np.linalg.norm(vec-old_pos)
        #print(distance)
        if distance<0.1:
            print("remove {} atom at position{}, index {}".format(new_geo.ion[i],old_pos,i))
            new_geo.remove_indices([i]) #delete ion at i index 
    return new_geo

def Insert_atom(geo,new_atom_name, new_atom_pos):
    """
    Insert the atom at crystal coordinate = new_atom_pos
    INPUT:
    Remove the atom at crystal coordinate=old_pos;
    INPUT:
        geo: geometry object load by :
            import pw2py as pw
            pw.atomgeo.from_file(fp, ftype='qeinp')
        new_atom_name: string
            name of the new atom
        new_atom_pos: 1x3 array or list
            atom position
    OUTPUT:
        geometry object; 
    """
    import numpy as np
    import copy
    new_geo=copy.deepcopy(geo)
    new_geo.add_atom((new_atom_name, new_atom_pos))
    return new_geo

def Write_all(Sup,name):
    """
    write the geo to output files, xsf, vasp and qe input
    Sup: geometry object
    name: filename (no postfix)
    """
    print("write to file...")
    # write some new file formats (will use extension but you can also use the ftype keyword)
    print("write to qe input")
    file_name="{}{}".format(name,'.in') #write to qe input
    Sup.write_file(file_name, ftype='qeinp')
    print("done")
    print("write to vasp")
    file_name="{}{}".format(name,'.vasp')#write to vasp
    Sup.write_file(file_name,sort=False)
    print('done')
    print("write to xsf")
    file_name="{}{}".format(name,'.xsf')# write to xsf
    Sup.write_file(file_name)
    print('done')
#write_atom(f_out,f_card)
