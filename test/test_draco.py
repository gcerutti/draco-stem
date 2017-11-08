# -*- coding: utf-8 -*-
# -*- python -*-
#
#       DRACO-STEM
#       Dual Reconstruction by Adjacency Complex Optimization
#       SAM Tissue Enhanced Mesh
#
#       Copyright 2014-2016 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Cerutti <guillaume.cerutti@inria.fr>
#
#       File contributor(s): Guillaume Cerutti <guillaume.cerutti@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenaleaLab Website : http://virtualplants.github.io/
#
###############################################################################

import numpy as np
from scipy import ndimage as nd

from vplants.container import array_dict

from vplants.cellcomplex.property_topomesh.property_topomesh_analysis import compute_topomesh_property
from vplants.cellcomplex.property_topomesh.utils.evaluation_tools import jaccard_index

from vplants.draco_stem.draco.draco import DracoMesh

from vplants.draco_stem.example_image import sphere_tissue_image

def test_draco():
    n_points = 12
    img = sphere_tissue_image(size=100,n_points=n_points)

    draco = DracoMesh(img)

    assert draco.point_topomesh.nb_wisps(0) == n_points+1

    draco.delaunay_adjacency_complex(surface_cleaning_criteria = [])

    image_tetrahedra = np.sort(draco.image_cell_vertex.keys())
    image_tetrahedra = image_tetrahedra[image_tetrahedra[:,0] != 1]
    draco_tetrahedra = np.sort([list(draco.triangulation_topomesh.borders(3,t,3)) for t in draco.triangulation_topomesh.wisps(3)])
    delaunay_consistency = jaccard_index(image_tetrahedra, draco_tetrahedra)

    draco.adjacency_complex_optimization(n_iterations=2)
    
    assert draco.triangulation_topomesh.nb_region_neighbors(0,2) == n_points

    image_tetrahedra = np.sort(draco.image_cell_vertex.keys())
    image_tetrahedra = image_tetrahedra[image_tetrahedra[:,0] != 1]
    draco_tetrahedra = np.sort([list(draco.triangulation_topomesh.borders(3,t,3)) for t in draco.triangulation_topomesh.wisps(3)])
    draco_consistency = jaccard_index(image_tetrahedra, draco_tetrahedra)

    # print delaunay_consistency,' -> ',draco_consistency

    assert draco_consistency == 1 or (draco_consistency >= 0.9 and draco_consistency > delaunay_consistency)

    triangular = ['star','remeshed','projected','regular','flat']
    image_dual_topomesh = draco.dual_reconstruction(reconstruction_triangulation = triangular, adjacency_complex_degree=3)

    image_volumes = array_dict(nd.sum(np.ones_like(img),img,index=np.unique(img)[1:])*np.prod(img.voxelsize),np.unique(img)[1:])
    compute_topomesh_property(image_dual_topomesh,'volume',3)
    draco_volumes = image_dual_topomesh.wisp_property('volume',3)

    for c in image_dual_topomesh.wisps(3):
        assert np.isclose(image_volumes[c],draco_volumes[c],0.33)


def test_draco_layer():
    n_points = 12
    img = sphere_tissue_image(size=100,n_points=n_points)

    draco = DracoMesh(img)

    draco.layer_adjacency_complex()

    triangular = ['star','remeshed','straight','regular',]
    image_dual_topomesh = draco.dual_reconstruction(reconstruction_triangulation = triangular, adjacency_complex_degree=2)

def test_draco_two_layers():
    n_points = 12
    img = sphere_tissue_image(size=100,n_points=n_points)

    draco = DracoMesh(img)

    draco.construct_adjacency_complex()

    triangular = ['star','remeshed','projected','regular','flat']
    image_dual_topomesh = draco.dual_reconstruction(reconstruction_triangulation = triangular, adjacency_complex_degree=3)





