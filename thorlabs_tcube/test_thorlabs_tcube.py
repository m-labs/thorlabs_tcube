import time
import sys
import unittest

from sipyco.test.generic_rpc import GenericRPCCase


class GenericTdcTest:
    def test_pot_parameters(self):
        test_vector = 1, 2, 3, 4, 5, 6, 7, 8
        self.cont.set_pot_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_pot_parameters())

    def test_position_counter(self):
        test_vector = 42
        self.cont.set_position_counter(test_vector)
        self.assertEqual(test_vector, self.cont.get_position_counter())

    def test_encoder_counter(self):
        test_vector = 43
        self.cont.set_encoder_counter(test_vector)
        self.assertEqual(test_vector, self.cont.get_encoder_counter())

    def test_velocity_parameters(self):
        test_vector = 44, 45
        self.cont.set_velocity_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_velocity_parameters())

    def test_jog_parameters(self):
        test_vector = 46, 47, 48, 49, 50
        self.cont.set_jog_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_jog_parameters())

    def test_gen_move_parameters(self):
        test_vector = 51
        self.cont.set_gen_move_parameters(test_vector)
        self.assertEqual(test_vector, self.cont.get_gen_move_parameters())

    def test_moverelparams(self):
        test_vector = 52
        self.cont.set_move_relative_parameters(test_vector)
        self.assertEqual(test_vector, self.cont.get_move_relative_parameters())

    def test_move_absolute_parameters(self):
        test_vector = 53
        self.cont.set_move_absolute_parameters(test_vector)
        self.assertEqual(test_vector, self.cont.get_move_absolute_parameters())

    def test_home_parameters(self):
        test_vector = 54
        self.cont.set_home_parameters(test_vector)
        self.assertEqual(test_vector, self.cont.get_home_parameters())

    def test_limit_switch_parameters(self):
        test_vector = 2, 1, 55, 56, 0x1
        self.cont.set_limit_switch_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_limit_switch_parameters())

    def test_dc_pid_parameters(self):
        test_vector = 57, 58, 59, 60, 0x0f
        self.cont.set_dc_pid_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_dc_pid_parameters())

    def test_av_modes(self):
        for i in range(1):
            for j in range(1):
                for k in range(1):
                    with self.subTest(i=i):
                        with self.subTest(j=j):
                            with self.subTest(k=k):
                                test_vector = i << 2 + j << 1 + k
                                self.cont.set_av_modes(test_vector)
                                self.assertEqual(test_vector,
                                                 self.cont.get_av_modes())

    def test_button_parameters(self):
        test_vector = 2, 3, 4
        self.cont.set_button_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_button_parameters())


class GenericTpzTest:
    def test_position_control_mode(self):
        test_vector = 1
        self.cont.set_position_control_mode(test_vector)
        self.assertEqual(test_vector, self.cont.get_position_control_mode())

    def test_output_volts(self):
        for voltage in 5.0, 10.0, 15.0, \
                round(self.cont.get_tpz_io_settings()[0]):
            with self.subTest(voltage=voltage):
                test_vector = voltage
                self.cont.set_output_volts(test_vector)
                time.sleep(1)  # Wait for the output voltage to converge
                self.assertAlmostEqual(test_vector,
                                       self.cont.get_output_volts(),
                                       delta=0.03)

    def test_output_position(self):
        test_vector = 31000
        self.cont.set_output_position(test_vector)
        self.assertEqual(test_vector, self.cont.get_output_position())

    def test_input_volts_source(self):
        for i in range(3):
            test_vector = i
            self.cont.set_input_volts_source(i)
            with self.subTest(i=i):
                self.assertEqual(test_vector,
                                 self.cont.get_input_volts_source())

    def test_pi_constants(self):
        test_vector = 42, 43
        self.cont.set_pi_constants(*test_vector)
        self.assertEqual(test_vector, self.cont.get_pi_constants())

    def test_tpz_display_settings(self):
        for intensity in 0, 10, 30, 50, 100, 150, 254:
            with self.subTest(intensity=intensity):
                test_vector = intensity
                self.cont.set_tpz_display_settings(test_vector)
                self.assertEqual(test_vector,
                                 self.cont.get_tpz_display_settings())

    def test_tpz_io_settings(self):
        for v in 75.0, 100.0, 150.0:
            with self.subTest(v=v):
                test_vector = v, 1
                self.cont.set_tpz_io_settings(*test_vector)
                self.assertEqual(test_vector, self.cont.get_tpz_io_settings())


class TestTdcSim(GenericRPCCase, GenericTdcTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (sys.executable.replace("\\", "\\\\")
                            + " -m thorlabs_tcube.aqctl_thorlabs_tcube "
                            + "-p 3255 -P tdc001 --simulation")
        self.cont = self.start_server("tdc", command, 3255)


class TestTpzSim(GenericRPCCase, GenericTpzTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (sys.executable.replace("\\", "\\\\")
                            + " -m thorlabs_tcube.aqctl_thorlabs_tcube "
                            + "-p 3255 -P tpz001 --simulation")
        self.cont = self.start_server("tpz", command, 3255)
