import numpy as np
import unittest

from numpy.ma.testutils import assert_array_equal

from flightdatautilities.array_operations import (
    downsample_arrays,
    mask_ratio,
    merge_masks,
    percent_unmasked,
    sum_arrays,
    upsample_arrays,
)


class TestMaskRatio(unittest.TestCase):
    def test_mask_ratio(self):
        self.assertEqual(mask_ratio(True), 1)
        self.assertEqual(mask_ratio(np.bool_(True)), 1)
        self.assertEqual(mask_ratio(False), 0)
        self.assertEqual(mask_ratio(np.bool_(False)), 0)
        array = np.ma.array(range(10))
        self.assertEqual(mask_ratio(np.ma.getmaskarray(array)), 0)
        array[0] = np.ma.masked
        self.assertEqual(mask_ratio(np.ma.getmaskarray(array)), 0.1)
        invalid_array = np.ma.array(range(100), mask=[True]*100)
        self.assertEqual(mask_ratio(np.ma.getmaskarray(invalid_array)), 1)


class TestMergeMasks(unittest.TestCase):
    def test_merge_masks(self):
        self.assertRaises(IndexError, merge_masks, [])
        self.assertEqual(
            merge_masks(np.array([[0,0,0]], dtype=np.bool_)).tolist(), False)
        self.assertEqual(
            merge_masks(np.array([[0,1,0]], dtype=np.bool_)).tolist(), [0,1,0])
        self.assertEqual(
            merge_masks(np.array([[1,1,1]], dtype=np.bool_)).tolist(), [1,1,1])
        self.assertEqual(
            merge_masks(np.array([[0,0,0],
                                  [0,0,0]], dtype=np.bool_)).tolist(), False)
        self.assertEqual(
            merge_masks(np.array([[0,1,0],
                                  [0,1,0]], dtype=np.bool_)).tolist(), [0,1,0])
        self.assertEqual(
            merge_masks(np.array([[0,1,0],
                                  [0,1,1]], dtype=np.bool_)).tolist(), [0,1,1])
        self.assertEqual(
            merge_masks(np.array([[1,1,1],
                                  [1,1,1]], dtype=np.bool_)).tolist(), [1,1,1])
        self.assertEqual(
            merge_masks(np.array([[1,0,0],
                                  [0,1,0],
                                  [0,0,1]], dtype=np.bool_)).tolist(), [1,1,1])


class TestSumArrays(unittest.TestCase):
    def test_merge_masks(self):
        self.assertRaises(IndexError, sum_arrays, [])
        self.assertEqual(
            sum_arrays(np.array([[0,0,0]])).tolist(), [0,0,0])
        self.assertEqual(
            sum_arrays(np.array([[0,1,0]])).tolist(), [0,1,0])
        self.assertEqual(
            sum_arrays(np.array([[1,1,1]])).tolist(), [1,1,1])
        self.assertEqual(
            sum_arrays(np.array([[0,0,0],
                                  [0,0,0]])).tolist(), [0,0,0])
        self.assertEqual(
            sum_arrays(np.array([[0,1,0],
                                  [0,1,0]])).tolist(), [0,2,0])
        self.assertEqual(
            sum_arrays(np.array([[0,1,0],
                                  [0,1,1]])).tolist(), [0,2,1])
        self.assertEqual(
            sum_arrays(np.array([[1,1,1],
                                  [1,1,1]])).tolist(), [2,2,2])
        self.assertEqual(
            sum_arrays(np.array([[1,0,0],
                                  [0,1,0],
                                  [0,0,1]])).tolist(), [1,1,1])


class TestDownsampleArrays(unittest.TestCase):
    def test_downsample_arrays(self):
        array1 = np.ma.arange(10)
        array2 = np.ma.arange(5)
        downsampled_array1, downsampled_array2 = downsample_arrays([array1,
                                                                    array2])
        assert_array_equal(downsampled_array1, np.ma.arange(0,10,2))
        assert_array_equal(downsampled_array2, array2)
        # With mask.
        array1[5:8] = np.ma.masked
        array2[2:4] = np.ma.masked
        downsampled_array1, downsampled_array2 = downsample_arrays([array1,
                                                                    array2])
        result_array1 = np.ma.arange(0,10,2)
        result_array1[3] = np.ma.masked
        assert_array_equal(downsampled_array1, result_array1)
        assert_array_equal(downsampled_array2, array2)


class TestUpsampleArrays(unittest.TestCase):
    def test_upsample_arrays(self):
        array1 = np.bool_(True)
        array2 = np.arange(5)
        upsampled_array1, upsampled_array2 = upsample_arrays([array1,
                                                              array2])
        assert_array_equal(upsampled_array1, np.array([array1] * 5))
        assert_array_equal(upsampled_array2, array2)
        
        array1 = np.ma.arange(10)
        array2 = np.ma.arange(5)
        upsampled_array1, upsampled_array2 = upsample_arrays([array1,
                                                              array2])
        assert_array_equal(upsampled_array1, array1)
        assert_array_equal(upsampled_array2, array2.repeat(2))
        # With mask.
        array1[5:8] = np.ma.masked
        array2[2:4] = np.ma.masked
        upsampled_array1, upsampled_array2 = upsample_arrays([array1,
                                                              array2])
        result_array2 = array2.repeat(2)
        result_array2[4:8] = np.ma.masked
        assert_array_equal(upsampled_array1, array1)
        assert_array_equal(upsampled_array2, result_array2)


class TestPercentUnmasked(unittest.TestCase):
    def test_mask_percentage(self):
        array = np.ma.array(range(10))
        self.assertEqual(percent_unmasked(np.ma.getmaskarray(array)), 100)
        array[0] = np.ma.masked
        self.assertEqual(percent_unmasked(np.ma.getmaskarray(array)), 90)
        invalid_array = np.ma.array(range(100), mask=[True]*100)
        self.assertEqual(percent_unmasked(np.ma.getmaskarray(invalid_array)), 0)