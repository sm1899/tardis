# atomic model

import os
import logging
import tardis
import numpy as np
import pandas as pd
import cPickle as pickle

from scipy import interpolate
from astropy import units, constants
from collections import OrderedDict
from pandas import DataFrame


class AtomDataNotPreparedError(Exception):
    pass


logger = logging.getLogger(__name__)

tardis_dir = os.path.dirname(os.path.realpath(tardis.__file__))

def data_path(fname):
    return os.path.join(tardis_dir, 'data', fname)

def tests_data_path(fname):
    return os.path.join(tardis_dir, 'tests', 'data', fname)


default_atom_h5_path = data_path('atom_data.h5')
atomic_symbols_data = np.recfromtxt(data_path('atomic_symbols.dat'),
                                    names=['atomic_number', 'symbol'])

symbol2atomic_number = OrderedDict(zip(atomic_symbols_data['symbol'],
                                       atomic_symbols_data['atomic_number']))
atomic_number2symbol = OrderedDict(atomic_symbols_data)

#
# @PendingDeprecationWarning
# def read_atomic_data(fname=None):
#     return read_basic_atom_data(fname)


# def read_hdf5_data(fname, dset_name):
#     """This function reads the dataset (dset_name) from the hdf5 file (fname).
#     In addition it uses the attribute 'units' and parses it to the `~astropy.table.Table` constructor.
#
#     Parameters
#     ----------
#
#     fname : `str`, optional
#         path to atomic.h5 file, if set to None it will read in default data directory
#
#     Returns
#     -------
#
#     data : `~astropy.table.Table`
#         returns the respective
#     """
#
#     h5_file = h5py.File(fname, 'r')
#     dataset = h5_file[dset_name]
#     data = np.asarray(dataset)
#     #    data_units = dataset.attrs['units']
#
#     data_table = table.Table(data)
#
#     #    for i, col_unit in enumerate(data_units):
#     #        if col_unit == 'n':
#     #            data_table.columns[i].units = None
#     #        elif col_unit == '1':
#     #            data_table.columns[i].units = units.Unit(1)
#     #        else:
#     #            data_table.columns[i].units = units.Unit(col_unit)
#
#     h5_file.close()
#
#     return data_table
#
#
# def read_basic_atom_data(fname=None):
#     """This function reads the atomic number, symbol, and mass from hdf5 file
#
#     Parameters
#     ----------
#
#     fname : `str`, optional
#         path to atomic.h5 file, if set to None it will read in default data directory
#
#     Returns
#     -------
#
#     data : `~astropy.table.Table`
#         table with fields z[1], symbol, mass[u]
#     """
#
#     data_table = read_hdf5_data(fname, 'basic_atom_data')
#     #    data_table.columns['mass'] = units.Unit('u').to('g', data_table['mass'])
#
#     return data_table
#
#
# def read_ionization_data(fname=None):
#     """This function reads the atomic number, ion number, and ionization energy from hdf5 file
#
#     Parameters
#     ----------
#
#     fname : `str`, optional
#         path to atomic.h5 file, if set to None it will read in default data directory
#
#     Returns
#     -------
#
#     data : `~astropy.table.Table`
#         table with fields z[1], ion[1], ionization_energy[eV]
#         .. note:: energy from unionized atoms to once-ionized atoms ion = 1, for once ionized
#                   to twice ionized ion=2, etc.
#     """
#
#     data_table = read_hdf5_data(fname, 'ionization_data')
#     #data_table.columns['ionization_energy'] = units.Unit('eV').to('erg', data_table.columns['ionization_energy'])
#
#     return data_table
#
#
# def read_levels_data(fname=None):
#     """This function reads atomic number, ion number, level_number, energy, g, metastable
#     information from hdf5 file.
#
#     Parameters
#     ----------
#
#     fname : `str`, optional
#         path to atomic.h5 file, if set to None it will read in default data directory
#
#     Returns
#     -------
#
#     data : `~astropy.table.Table`
#         table with fields z[1], ion[1], level_number, energy, g, metastable
#     """
#
#     data_table = read_hdf5_data(fname, 'levels_data')
#     #data_table.columns['energy'].convert_units_to('erg')
#     #data_table.columns['energy'] = units.Unit('eV').to('erg', data_table.columns['energy'])
#
#
#     return data_table
#
#
# def read_synpp_refs(fname):
#     data_table = h5py.File(fname, 'r')['synpp_refs']
#
#     return data_table.__array__()
#
#
# def read_lines_data(fname=None):
#     """
#     This function reads the wavelength, atomic number, ion number, f_ul, f_l and level id information
#      from hdf5 file
#
#     Parameters
#     ----------
#
#     fname : `str`, optional
#         path to atomic.h5 file, if set to None it will read in default data directory
#
#     Returns
#     -------
#
#     data : `~astropy.table.Table`
#         table with fields wavelength, atomic_number, ion_number, f_ul, f_lu, level_id_lower, level_id_upper.
#     """
#
#     data_table = read_hdf5_data(fname, 'lines_data')
#     #data_table.columns['ionization_energy'].convert_units_to('erg')
#
#     return data_table
#
#
# def read_zeta_data(fname):
#     """
#     This function reads the recombination coefficient data from the HDF5 file
#
#
#     :return:
#     """
#
#     if fname is None:
#         raise ValueError('fname can not be "None" when trying to use NebularAtom')
#
#     if not os.path.exists(fname):
#         raise IOError('HDF5 File doesn\'t exist')
#
#     h5_file = h5py.File(fname, 'r')
#
#     if 'zeta_data' not in h5_file.keys():
#         raise ValueError('zeta_data not available in this HDF5-data file. It can not be used with NebularAtomData')
#
#     zeta_data = h5_file['zeta_data']
#     t_rads = zeta_data.attrs['t_rad']
#     return pd.DataFrame(zeta_data[:,2:], index=pd.MultiIndex.from_arrays(zeta_data[:,:2].transpose().astype(int)),
#                  columns=t_rads)
#
#
# def read_collision_data(fname):
#     if fname is None:
#         raise ValueError('fname can not be "None" when trying to use NebularAtom')
#
#     if not os.path.exists(fname):
#         raise IOError('HDF5 File doesn\'t exist')
#
#     h5_file = h5py.File(fname, 'r')
#
#     if 'collision_data' not in h5_file.keys():
#         raise ValueError('collision_data not available in this HDF5-data file. It can not be used with NLTE')
#
#     collision_data = np.array(h5_file['collision_data'])
#     collision_temperatures = h5_file['collision_data'].attrs['temperatures']
#
#     return collision_data, collision_temperatures
#
#
# def read_ion_cx_data(fname):
#     try:
#         h5_file = h5py.File(fname, 'r')
#         ion_cx_th_data = h5_file['ionization_cx_threshold']
#         ion_cx_sp_data = h5_file['ionization_cx_support']
#         return ion_cx_th_data, ion_cx_sp_data
#     except IOError, err:
#         print(err.errno)
#         print(err)
#         logger.critical('Cannot import. Error opening the file to read ionization_cx')
#
#
# def read_macro_atom_data(fname):
#     if fname is None:
#         raise ValueError('fname can not be "None" when trying to use NebularAtom')
#
#     if not os.path.exists(fname):
#         raise IOError('HDF5 File doesn\'t exist')
#
#     h5_file = h5py.File(fname, 'r')
#
#     if 'macro_atom_data' not in h5_file.keys():
#         raise ValueError('Macro Atom Data (macro_atom_data) is not in this HDF5-data file. '
#                          'It is needed for complex line interaction')
#     macro_atom_data = h5_file['macro_atom_data']
#
#     macro_atom_counts = h5_file['macro_atom_references']
#
#     return macro_atom_data, macro_atom_counts


class AtomData(object):
    """
    Class for storing atomic data

    AtomData
    ---------

    Parameters
    ----------

    basic_atom_data : `~astropy.table.Table`
        containing the basic atom data: z, symbol, and mass

    ionization_data : ~astropy.table.Table
        containing the ionization data: z, ion, and ionization energy
        ::important to note here is that ion describes the final ion state
            e.g. H I - H II is described with ion=2

    levels : ~astropy.table.Table
        containing the levels data: z, ion, level_number, energy, g

    lines : ~astropy.table.Table
        containing the lines data: wavelength, z, ion, levels_number_lower,
        levels_number_upper, f_lu, f_ul

    macro_atom_data : tuple of ~astropy.table.Table
        default ~None, a tuple of the macro-atom data and macro-atom references

    zeta_data : ~dict of interpolation objects
        default ~None

    """

    @classmethod
    def from_hdf5(cls, fname=None):
        """
        Function to read all the atom data from a special TARDIS HDF5 File.

        Parameters
        ----------

        fname: str, optional
            the default for this is `None` and then it will use the very limited atomic_data shipped with TARDIS
            For more complex atomic data please contact the authors.

        use_macro_atom:
            default `False`. Set to `True`, if you want to read in macro_atom_data
        """

        if fname is None:
            fname = default_atom_h5_path

        if not os.path.exists(fname):
            raise ValueError("Supplied Atomic Model Database %s does not exists" % fname)

        with pd.HDFStore(fname) as store:

            try:
                basic_atom_df = store["basic_atom_df"]
            except KeyError:
                print "Basic atom data is not available in this HDF5-data file."
                basic_atom_df = None

            try:
                ionization_df = store["ionization_df"]
            except KeyError:
                print "Ionization data is not available in this HDF5-data file."
                ionization_df = None

            try:
                levels_df = store["levels_df"]
            except KeyError:
                print "Levels data is not available in this HDF5-data file."
                levels_df = None

            try:
                lines_df = store["lines_df"]
            except KeyError:
                print "Lines data is not available in this HDF5-data file"
                lines_df = None

            try:
                macro_atom_df = store["macro_atom_df"]
            except KeyError:
                print "Macro atom data is not available in this HDF5-data file."
                macro_atom_df = None

            try:
                macro_atom_ref_df = store["macro_atom_ref_df"]
            except KeyError:
                print "Macro atom reference data is not available in this HDF5-data file."
                macro_atom_ref_df = None

            try:
                zeta_data = store["zeta_data"]
            except KeyError:
                print "Zeta data is not available in this HDF5-data file."
                zeta_data = None

            try:
                collisions_df = store["collisions_df"]
                collisions_temperatures = store.get_storer("collisions_df").attrs["temperatures"]
            except KeyError:
                print "Collision data is not available in this HDF5-data file."
                collisions_df, collisions_temperatures = (None, None)

            try:
                synpp_refs = store["synpp_refs"]
            except KeyError:
                print "Synpp refs is not available in this HDF5-data file."
                synpp_refs = None

            try:
                ion_cx_df = store["ion_cx_df"]
            except KeyError:
                print "Ionization cx data is not available in this HDF5-data file."
                ion_cx_df = None

            atom_data = cls(atom_data=basic_atom_df, ionization_data=ionization_df, levels_data=levels_df,
                            lines_data=lines_df, macro_atom_data=(macro_atom_df, macro_atom_ref_df), zeta_data=zeta_data,
                            collision_data=(collisions_df, collisions_temperatures), synpp_refs=synpp_refs,
                            ion_cx_data=ion_cx_df)

            atom_data.uuid1 = store.root._v_args.attrs['uuid1']
            atom_data.md5 = store.root._v_args.attrs['md5']

            try:
                atom_data.version = store.root._v_args.attrs['database_version']
            except KeyError:
                atom_data.version = None

            # ToDo: strore data sources as attributes in carsus
            # if atom_data.version is not None:
            #     atom_data.data_sources = pickle.loads(h5_file.attrs['data_sources'])

            logger.info('Read Atom Data with UUID=%s and MD5=%s', atom_data.uuid1, atom_data.md5)

        return atom_data

    def __init__(self, atom_data, ionization_data, levels_data, lines_data, macro_atom_data=None, zeta_data=None,
                 collision_data=None, synpp_refs=None, ion_cx_data=None):

        self.prepared = False

        self.atom_data = atom_data
        # We have to use constants.u because astropy uses different values for the unit u and the constant.
        # This is changed in later versions of astropy (the value of constants.u is used in all cases)
        if units.u.cgs == constants.u.cgs:
            self.atom_data["mass"] = units.Quantity(self.atom_data["mass"].values, "u").cgs
        else:
            self.atom_data["mass"] = self.atom_data["mass"].values * constants.u.cgs

        self.ionization_data = ionization_data
        self.ionization_data["ionization_energy"] = units.Quantity(self.ionization_data["ionization_energy"].values, "eV").cgs

        if levels_data is not None:
            self.levels = levels_data
            self.levels["energy"] = units.Quantity(self.levels["energy"].values, 'eV').cgs
            self.has_levels = True
        else:
            self.has_levels = False

        if lines_data is not None:
            self.lines['wavelength_cm'] = units.Quantity(self.lines['wavelength'], 'angstrom').cgs
            self.has_lines = True
        else:
            self.has_lines = False

        if macro_atom_data is not None:
            self.macro_atom_data_all, self.macro_atom_references_all = macro_atom_data
            self.has_macro_atom = True
        else:
            self.has_macro_atom = False

        # if ion_cx_data is not None:
        #     self.has_ion_cx_data = True
        #     #TODO:Farm a panda here
        #     self.ion_cx_th_data = DataFrame(np.array(ion_cx_data[0]))
        #     self.ion_cx_th_data.set_index(['atomic_number', 'ion_number', 'level_id'], inplace=True)
        #
        #     self.ion_cx_sp_data = DataFrame(np.array(ion_cx_data[1]))
        #     self.ion_cx_sp_data.set_index(['atomic_number', 'ion_number', 'level_id'])
        # else:
        #     self.has_ion_cx_data = False

        # if zeta_data is not None:
        #     self.zeta_data = zeta_data
        #     self.has_zeta_data = True
        # else:
        #     self.has_zeta_data = False

        if collision_data[0] is not None:
            self.collision_data, self.collision_data_temperatures = collision_data
            self.has_collision_data = True
        else:
            self.has_collision_data = False

        # if synpp_refs is not None:
        #     self.has_synpp_refs = True
        #     self.synpp_refs = pd.DataFrame(synpp_refs)
        #     self.synpp_refs.set_index(['atomic_number', 'ion_number'], inplace=True)
        #
        # else:
        #     self.has_synpp_refs = False

        self.symbol2atomic_number = OrderedDict(zip(self.atom_data['symbol'].values, self.atom_data.index))
        self.atomic_number2symbol = OrderedDict(zip(self.atom_data.index, self.atom_data['symbol']))


    def prepare_atom_data(self, selected_atomic_numbers, line_interaction_type='scatter', max_ion_number=None,
                          nlte_species=[]):
        """
        Prepares the atom data to set the lines, levels and if requested macro atom data.
        This function mainly cuts the `levels` and `lines` by discarding any data that is not needed (any data
        for atoms that are not needed

        Parameters
        ----------

        selected_atoms : `~set`
            set of selected atom numbers, e.g. set([14, 26])

        line_interaction_type : `~str`
            can be 'scatter', 'downbranch' or 'macroatom'

        max_ion_number : `~int`
            maximum ion number to be included in the calculation

        """
        if not self.prepared:
            self.prepared = True
        else:
            raise AtomDataNotPreparedError("AtomData was already prepared")
        self.selected_atomic_numbers = selected_atomic_numbers

        self.nlte_species = nlte_species
        self.levels = self.levels.reset_index(drop=True)

        self.levels = self.levels[self.levels['atomic_number'].isin(self.selected_atomic_numbers)]

        if max_ion_number is not None:
            self.levels = self.levels[self.levels['ion_number'] <= max_ion_number]

        self.levels = self.levels.set_index(['atomic_number', 'ion_number', 'level_number'])


        self.levels_index = pd.Series(np.arange(len(self.levels), dtype=int), index=self.levels.index)
        #cutting levels_lines
        self.lines = self.lines[self.lines['atomic_number'].isin(self.selected_atomic_numbers)]
        if max_ion_number is not None:
            self.lines = self.lines[self.lines['ion_number'] <= max_ion_number]

        # self.lines.sort(['wavelength', 'line_id'], inplace=True)
        self.lines.sort(['wavelength'], inplace=True)
        self.lines.set_index('line_id', inplace=True)



        self.lines_index = pd.Series(np.arange(len(self.lines), dtype=int), index=self.lines.index)

        tmp_lines_lower2level_idx = pd.MultiIndex.from_arrays([self.lines['atomic_number'], self.lines['ion_number'],
                                                               self.lines['level_number_lower']])

        self.lines_lower2level_idx = self.levels_index.ix[tmp_lines_lower2level_idx].values.astype(np.int64)

        tmp_lines_upper2level_idx = pd.MultiIndex.from_arrays([self.lines['atomic_number'], self.lines['ion_number'],
                                                               self.lines['level_number_upper']])

        self.lines_upper2level_idx = self.levels_index.ix[tmp_lines_upper2level_idx].values.astype(np.int64)

        self.atom_ion_index = None
        self.levels_index2atom_ion_index = None

        if self.has_macro_atom and not (line_interaction_type == 'scatter'):
            self.macro_atom_data = self.macro_atom_data_all[
                self.macro_atom_data_all['atomic_number'].isin(self.selected_atomic_numbers)]

            if max_ion_number is not None:
                self.macro_atom_data = self.macro_atom_data[self.macro_atom_data['ion_number'] <= max_ion_number]

            self.macro_atom_references = self.macro_atom_references_all[
                self.macro_atom_references_all['atomic_number'].isin(
                    self.selected_atomic_numbers)]
            if max_ion_number is not None:
                self.macro_atom_references = self.macro_atom_references[
                    self.macro_atom_references['ion_number'] <= max_ion_number]

            if line_interaction_type == 'downbranch':
                self.macro_atom_data = self.macro_atom_data[(self.macro_atom_data['transition_type'] == -1).values]

                self.macro_atom_references = self.macro_atom_references[self.macro_atom_references['count_down'] > 0]
                self.macro_atom_references['count_total'] = self.macro_atom_references['count_down']
                self.macro_atom_references['block_references'] = np.hstack((0,
                                                                            np.cumsum(self.macro_atom_references[
                                                                                          'count_down'].values[:-1])))
            elif line_interaction_type == 'macroatom':
                block_references = np.hstack((0, np.cumsum(
                    self.macro_atom_references['count_total'].values[:-1])))
                self.macro_atom_references.insert(len(
                    self.macro_atom_references.columns), 'block_references',
                    pd.Series(block_references,
                    index=self.macro_atom_references.index))

            self.macro_atom_references.set_index(['atomic_number', 'ion_number', 'source_level_number'], inplace=True)
            self.macro_atom_references.insert(len(
                    self.macro_atom_references.columns), 'references_idx',
                    pd.Series(np.arange(len(self.macro_atom_references)),
                    index=self.macro_atom_references.index))

            self.macro_atom_data.insert(len(
                self.macro_atom_data.columns), 'lines_idx',
                pd.Series(self.lines_index.ix[self.macro_atom_data[
                'transition_line_id']].values,
                index=self.macro_atom_data.index))

            tmp_lines_upper2level_idx = pd.MultiIndex.from_arrays(
                [self.lines['atomic_number'], self.lines['ion_number'],
                 self.lines['level_number_upper']])

            self.lines_upper2macro_reference_idx = self.macro_atom_references['references_idx'].ix[
                tmp_lines_upper2level_idx].values.astype(np.int64)

            tmp_macro_destination_level_idx = pd.MultiIndex.from_arrays([self.macro_atom_data['atomic_number'],
                                                                         self.macro_atom_data['ion_number'],
                                                                         self.macro_atom_data[
                                                                             'destination_level_number']])

            if line_interaction_type == 'macroatom':
                #Sets all

                self.macro_atom_data.insert(len(
                    self.macro_atom_data.columns), 'destination_level_idx',
                    pd.Series(self.macro_atom_references['references_idx'].ix[
                    tmp_macro_destination_level_idx].values.astype(
                        np.int64), index=self.macro_atom_data.index))

            elif line_interaction_type == 'downbranch':
                # Sets all the destination levels to -1 to indicate that they
                # are not used in downbranch calculations
                self.macro_atom_data.loc[:, 'destination_level_idx'] = (
                    np.ones(len(self.macro_atom_data)) * -1).astype(np.int64)

        self.nlte_data = NLTEData(self, nlte_species)


    def __repr__(self):
        return "<Atomic Data UUID=%s MD5=%s Lines=%d Levels=%d>" % \
               (self.uuid1, self.md5, self.lines.atomic_number.count(), self.levels.energy.count())


class NLTEData(object):
    def __init__(self, atom_data, nlte_species):
        self.atom_data = atom_data
        self.lines = atom_data.lines.reset_index(drop=True)
        self.nlte_species = nlte_species

        if nlte_species:
            logger.info('Preparing the NLTE data')
            self._init_indices()
            self._create_nlte_mask()
            if atom_data.has_collision_data:
                self._create_collision_coefficient_matrix()
        else:
            self._create_nlte_mask()

    def _init_indices(self):
        self.lines_idx = {}
        self.lines_level_number_lower = {}
        self.lines_level_number_upper = {}
        self.A_uls = {}
        self.B_uls = {}
        self.B_lus = {}

        for species in self.nlte_species:
            lines_idx = np.where((self.lines.atomic_number == species[0]) &
                                 (self.lines.ion_number == species[1]))
            self.lines_idx[species] = lines_idx
            self.lines_level_number_lower[species] = self.lines.level_number_lower.values[lines_idx].astype(int)
            self.lines_level_number_upper[species] = self.lines.level_number_upper.values[lines_idx].astype(int)

            self.A_uls[species] = self.atom_data.lines.A_ul.values[lines_idx]
            self.B_uls[species] = self.atom_data.lines.B_ul.values[lines_idx]
            self.B_lus[species] = self.atom_data.lines.B_lu.values[lines_idx]

    def _create_nlte_mask(self):
        self.nlte_levels_mask = np.zeros(self.atom_data.levels.energy.count()).astype(bool)
        self.nlte_lines_mask = np.zeros(self.atom_data.lines.wavelength.count()).astype(bool)

        for species in self.nlte_species:
            current_levels_mask = (self.atom_data.levels.index.get_level_values(0) == species[0]) & \
                           (self.atom_data.levels.index.get_level_values(1) == species[1])
            current_lines_mask = (self.atom_data.lines.atomic_number.values == species[0]) & \
                           (self.atom_data.lines.ion_number.values == species[1])
            self.nlte_levels_mask |= current_levels_mask
            self.nlte_lines_mask |= current_lines_mask


    def _create_collision_coefficient_matrix(self):
        self.C_ul_interpolator = {}
        self.delta_E_matrices = {}
        self.g_ratio_matrices = {}
        collision_group = self.atom_data.collision_data.groupby(level=['atomic_number', 'ion_number'])
        for species in self.nlte_species:
            no_of_levels = self.atom_data.levels.ix[species].energy.count()
            C_ul_matrix = np.zeros((no_of_levels, no_of_levels, len(self.atom_data.collision_data_temperatures)))
            delta_E_matrix = np.zeros((no_of_levels, no_of_levels))
            g_ratio_matrix = np.zeros((no_of_levels, no_of_levels))

            for (atomic_number, ion_number, level_number_lower, level_number_upper), line in \
                collision_group.get_group(species).iterrows():
                C_ul_matrix[level_number_lower, level_number_upper, :] = line.values[2:]
                delta_E_matrix[level_number_lower, level_number_upper] = line['delta_e']
                #TODO TARDISATOMIC fix change the g_ratio to be the otherway round - I flip them now here.
                g_ratio_matrix[level_number_lower, level_number_upper] = line['g_ratio']
            self.C_ul_interpolator[species] = interpolate.interp1d(self.atom_data.collision_data_temperatures,
                                                                   C_ul_matrix)
            self.delta_E_matrices[species] = delta_E_matrix

            self.g_ratio_matrices[species] = g_ratio_matrix


    def get_collision_matrix(self, species, t_electrons):
        c_ul_matrix = self.C_ul_interpolator[species](t_electrons)
        no_of_levels = c_ul_matrix.shape[0]
        c_ul_matrix[np.isnan(c_ul_matrix)] = 0.0

        #TODO in tardisatomic the g_ratio is the other way round - here I'll flip it in prepare_collision matrix

        c_lu_matrix = c_ul_matrix * np.exp(-self.delta_E_matrices[species].reshape((no_of_levels, no_of_levels, 1)) /
                                           t_electrons.reshape((1, 1, t_electrons.shape[0]))) * \
                      self.g_ratio_matrices[species].reshape((no_of_levels, no_of_levels, 1))
        return c_ul_matrix + c_lu_matrix.transpose(1, 0, 2)
